import string
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from factory import LazyAttribute, lazy_attribute, SubFactory, Iterator
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory

from ..models import WildBillsProfile, Organization, PaymentFrequency, Debt, Bill

__author__ = 'luiscberrocal'

faker = FakerFactory.create()


class WildBillsProfileFactory(DjangoModelFactory):

    class Meta:
        model = WildBillsProfile

    first_name = LazyAttribute(lambda x: faker.first_name())
    last_name = LazyAttribute(lambda x: faker.last_name())
    password = 'user1'
    country = 'PA'

    @lazy_attribute
    def username(self):
        return '%s.%s' % (self.first_name.lower(), self.last_name.lower())

    @lazy_attribute
    def email(self):
        return '%s@example.com' % self.username

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(WildBillsProfileFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class OrganizationFactory(DjangoModelFactory):

    class Meta:
        model = Organization

    owner = SubFactory(WildBillsProfileFactory)

    @lazy_attribute
    def legal_name(self):
        return self.display_name
    
    @lazy_attribute
    def display_name(self):
        if self.owner.last_name:
            last_name = self.owner.last_name
        else:
            last_name = faker.last_name()
        return 'Family %s' % last_name


class MonthlyPaymentFrequencyFactory(DjangoModelFactory):

    class Meta:
        model = PaymentFrequency

    frequency_values = Iterator(['30', '15, 30', '5'])
    frequency = LazyAttribute(lambda x: PaymentFrequency.FREQ_MONTHLY)
    start_date = timezone.now()


class MonthlyDebtFactory(DjangoModelFactory):

    class Meta:
        model = Debt

    payee = LazyAttribute(lambda x: faker.company())
    description = LazyAttribute(lambda x: faker.text(max_nb_chars=200))
    amount = 100.0
    frequency = SubFactory(MonthlyPaymentFrequencyFactory)
    organization = SubFactory(OrganizationFactory)


class MonthlyBillFactory(DjangoModelFactory):

    class Meta:
        model = Bill

    debt = SubFactory(MonthlyDebtFactory)
    due_date = faker.date_time_between(start_date="now", end_date="+1y")

    @lazy_attribute
    def amount(self):
        return self.debt.amount











