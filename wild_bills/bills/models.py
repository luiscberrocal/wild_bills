from datetime import date
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.utils import timezone
from model_utils.models import TimeStampedModel

from ..categories.models import Category
from .managers import BillManager, DebtManager
from .utils import frequency_calculator
import logging

logger = logging.getLogger(__name__)


# class WildBillsProfile(AbstractUser):
#     country = CountryField(verbose_name= _('Country'))


class Organization(models.Model):
    display_name = models.CharField(_('Display name'), max_length=150,
                                    help_text=_("Name that you communicate"))
    legal_name = models.CharField(_('Legal name'), max_length=150, blank=True,
                                  help_text=_("Official name. Only relevant if the organization is a company"))

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="owned_organizations",
                              verbose_name=_('Owner'))
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name="organizations",
                                     verbose_name=_('Members') )

    class Meta:
        pass

    def __str__(self):
        return self.display_name


class PaymentFrequency(models.Model):
    FREQ_MONTHLY = 'Monthly'
    FREQ_WEEKLY = 'Weekly'
    FREQ_BIWEEKLY = 'Biweekly'
    FREQ_CHOICES = (
        (FREQ_MONTHLY, _('Monthly')),
        (FREQ_WEEKLY, _('Weekly')),
        (FREQ_BIWEEKLY, _('Biweekly'))
    )
    frequency_values = models.CharField(_('Frequency values'), max_length=60, blank=True,
                                        help_text=_('Which days of the month or days of the week the payment '
                                                    'should occur. Values separated by comma'))
    frequency = models.CharField(_('Frequency'), max_length=15, choices=FREQ_CHOICES, default=FREQ_MONTHLY)
    start_date = models.DateField(_('Start date'), null=True, blank=True)

    def get_days_of_the_month(self):
        day_list = list()
        if self.frequency_values:
            str_days = self.frequency_values.split(',')
            for str_day in str_days:
                day_list.append(int(str_day))
        return sorted(day_list)

    def calculate_next_date(self, ref_date):
        if self.frequency == self.FREQ_MONTHLY:
            days_list = self.get_days_of_the_month()
            next_date = frequency_calculator.get_next_closest(ref_date, days_list)
            return next_date

        else:
            raise NotImplementedError('Only montly frequency is supported')

    def __str__(self):
        if self.frequency == self.FREQ_MONTHLY:
            return _('Pay every month on %s of the month') % self.frequency_values
        elif self.frequency == self.FREQ_WEEKLY:
            return _('Pay every week on %s') % self.frequency_values
        elif self.frequency == self.FREQ_BIWEEKLY:
            return _('Pay every two weeks on %s') % self.frequency_values
        else:
            return _('No frequency has been selected')


class Debt(TimeStampedModel):
    payee = models.CharField(_('Payee'), max_length=150)
    description = models.CharField(_('Description'), max_length=255)
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2)
    fixed_amount = models.BooleanField(_('Fixed amount'), default=False)
    organization = models.ForeignKey(Organization, related_name='debts',
                                     verbose_name=_('Organization'))
    frequency = models.ForeignKey(PaymentFrequency,
                                  verbose_name=_('Frequency'))
    end_date = models.DateField(_('End date'), null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=_('Category'),
                                 related_name='debts', null=True, blank=True)

    objects = DebtManager()

    def get_absolute_url(self):
        return reverse('bills:debt-detail', args=[self.pk])

    def create_bills(self, count=2):
        bills_created = list()
        last_bill = Bill.objects.filter(debt=self).order_by('-due_date').first()
        if last_bill:
            start_date = last_bill.due_date
        else:
            start_date = timezone.now().date()
        for c in range(1,count+1):
            if self.frequency.frequency == self.frequency.FREQ_MONTHLY:
                due_date = self.frequency.calculate_next_date(start_date)
                logger.debug('Adding %d bill for %s' % (c, due_date.strftime('%Y-%m-%d')))
                new_bill = Bill.objects.create(debt=self, amount=self.amount, due_date=due_date)
                bills_created.append(new_bill)
                start_date = due_date
            else:
                raise NotImplementedError('Only monthly frequency is supported to create bills')
        return bills_created


class Payment(models.Model):

    amount = models.DecimalField(_('Amount'),
                                 decimal_places=2,
                                 max_digits=12)
    detail = models.CharField(_('Detail'), max_length=255,
                              blank=True,
                              null=True)
    date_paid = models.DateField(_('Date paid'), default=date.today)
    reference = models.CharField(_('Reference'), max_length=255,
                                 blank=True,
                                 null=True)


    class Meta:
        ordering = ('-date_paid',)

    def __str__(self):
        if self.detail:
            return self.detail
        return _("Payment of {}").format(self.amount)


class Bill(TimeStampedModel):
    STATUS_UNPAID = 'UNPAID'
    STATUS_PAID = 'PAID'
    STATUS_UNDER_PAID = 'UNDER_PAID'
    STATUS_OVER_PAID = 'OVER_PAID'
    STATUS_CHOICES = (
        (STATUS_UNPAID, _('Unpaid')),
        (STATUS_PAID, _('Paid')),
        (STATUS_UNDER_PAID, _('Under paid')),
        (STATUS_OVER_PAID, _('Over paid'))
    )
    debt = models.ForeignKey(Debt, related_name='debts', verbose_name=_('Debt'))
    amount = models.DecimalField(_('Amount'),
                                 decimal_places=2,
                                 max_digits=12)
    due_date = models.DateField(_('Due date'))
    payments = models.ManyToManyField(Payment, related_name='bills', verbose_name=_('Payments'))
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default=STATUS_UNPAID)
    objects = BillManager()

    def amount_paid(self):
        total_paid = Payment.objects.filter(bills=self).aggregate(Sum('amount'))
        return total_paid['amount__sum']

    def set_status(self):
        total_paid = self.amount_paid()
        if total_paid == self.amount:
            self.status = self.STATUS_PAID
        elif total_paid > self.amount:
            self.status = self.STATUS_OVER_PAID
        elif total_paid < self.amount and self.amount != 0:
            self.status = self.STATUS_UNDER_PAID
        else:
            self.status = self.STATUS_UNPAID

    def pay(self, amount=0.0, date_paid=timezone.now().date()):
        if amount == 0.0:
            amount = self.amount
        payment_sum = Payment.objects.filter(bills=self).aggregate(Sum('amount'))
        if payment_sum['amount__sum']is None or payment_sum['amount__sum'] < self.amount:
            payment = Payment.objects.create(amount=amount, date_paid=date_paid)
            self.payments.add(payment)
            self.set_status()
            self.save()
            return payment
        elif payment_sum['amount__sum'] >= self.amount:
            return None

    def amount_due(self):
        payment_sum = Payment.objects.filter(bills=self).aggregate(Sum('amount'))
        if payment_sum['amount__sum']is None:
            return self.amount
        else:
            return  Decimal(self.amount) -payment_sum['amount__sum']

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super(Bill, self).save(force_insert=force_insert, force_update=force_update,
    #                                   using=using, update_fields=update_fields)
    #     self.set_status()
    #     return super(Bill, self).save(force_insert=force_insert, force_update=force_update,
    #                                   using=using, update_fields=update_fields)

    class Meta:
        unique_together = ('debt', 'due_date')


