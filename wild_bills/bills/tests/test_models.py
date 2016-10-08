from datetime import date

from django.db.models import Q
from django.test import TestCase
from django.utils import translation, timezone

from ...users.tests.factories import UserFactory
from ..utils import frequency_calculator
from ..models import Organization, Debt, PaymentFrequency, Bill
from .factories import OrganizationFactory, MonthlyDebtFactory, MonthlyPaymentFrequencyFactory, \
    MonthlyBillFactory


class TestWilbBillsProfile(TestCase):

    def test_create(self):
        translation.activate('en')
        profile = UserFactory.create()
        country_name = str(profile.country.name)
        self.assertEqual('Panama', country_name)
        #self.assertEqual(1, Organization.objects.count())

    def test_create_with_username(self):
        username = 'obiwan'
        password = 'password'
        profile = UserFactory.create(username=username,
                                                      password=password,
                                                      email='obiwan@jedi.org')
        self.assertEqual(username, profile.username)


    def test_members_create(self):
        profile = UserFactory.create()
        organization = OrganizationFactory.create(owner=profile)
        self.assertEqual(0, organization.members.count())
        profile2 = UserFactory.create()
        owned_org = profile.owned_organizations.all()[0]
        owned_org.members.add(profile2)
        owned_org.save()
        self.assertEqual(1, organization.members.count())


class TestOrganization(TestCase):

    def test_create(self):
        organization = OrganizationFactory.create()
        self.assertEqual(1, Organization.objects.count())
        self.assertIsNotNone(organization.owner)


class TestDebt(TestCase):

    def test_create_monthly(self):
        debt = MonthlyDebtFactory.create()
        self.assertEqual(1, Debt.objects.count())

    def test_create_batch_monthly(self):
        debt = MonthlyDebtFactory.create_batch(5)
        self.assertEqual(5, Debt.objects.count())

    def test_create_batch_different_users(self):
        profile = UserFactory.create()
        organization = OrganizationFactory.create(owner=profile)
        MonthlyDebtFactory.create_batch(10, organization=organization)
        MonthlyDebtFactory.create_batch(5)
        self.assertEqual(15, Debt.objects.count())
        self.assertEqual(10, Debt.objects.filter(organization=organization).count())

    def test_create_bills(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create(start_date=date(2015,10,14),
                                                                  frequency_values='15,30')
        debt = MonthlyDebtFactory.create(frequency=payment_frequency)
        self.assertEqual(0, Bill.objects.count())
        debt.create_bills(3)
        self.assertEqual(3, Bill.objects.count())
        expected_dates = self._get_expected_dates(3, [15,30]) #[date(2015,10,15), date(2015,10,30), date(2015, 11, 15)]
        bills = Bill.objects.all().order_by('due_date')
        c = 0
        for bill in bills:
            self.assertEqual(bill.due_date, expected_dates[c])
            c += 1

    def _get_expected_dates(self, count, days_list):
        expected_dates = list()
        current_date = timezone.now().date()
        for i in range(0, count):
            next_date = frequency_calculator.get_next_closest(current_date, days_list)
            expected_dates.append(next_date)
            current_date = next_date
        return expected_dates

    def test_create_bills_twice(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create(start_date=date(2015,10,14),
                                                                  frequency_values='15,30')
        debt = MonthlyDebtFactory.create(frequency=payment_frequency)
        self.assertEqual(0, Bill.objects.count())
        debt.create_bills(3)
        self.assertEqual(3, Bill.objects.count())
        debt.create_bills(3)
        self.assertEqual(6, Bill.objects.count())
        expected_dates = self._get_expected_dates(6, [15, 30])
        bills = Bill.objects.all().order_by('due_date')
        c = 0
        for bill in bills:
            self.assertEqual(bill.due_date, expected_dates[c])
            c += 1

    def test_without_outstanding_bills(self):
        '''
        1. create 10 debts for an organization.
        2. creat a bill for the first debt
        3. create a bill for the second debt
        4. create 2 bills for the third debt
        5. Pay in full the first bill
        6. Create 5 more debts
        There should only be 2 debts with upaid or under paid bills
        :return:
        '''
        profile = UserFactory.create()
        organization = OrganizationFactory.create(owner=profile)
        created_debts = MonthlyDebtFactory.create_batch(10, organization=organization)
        bills_created = created_debts[0].create_bills(1)
        created_debts[1].create_bills(1)
        created_debts[2].create_bills(2)
        bills_created[0].pay()
        MonthlyDebtFactory.create_batch(5)

        unpaid_debts_ids = Bill.objects.filter(Q(debt__organization=organization),
                                               Q(status=Bill.STATUS_UNPAID) | Q(status=Bill.STATUS_UNDER_PAID))
        unpaid_debts_ids = unpaid_debts_ids.distinct('debt').values('debt__pk')
        self.assertEqual(2, len(unpaid_debts_ids))
        debts = Debt.objects.filter(organization=organization).exclude(pk__in=unpaid_debts_ids)
        self.assertEqual(8, len(debts))

        debts2 = Debt.objects.without_outstanding_bills(organization=organization)
        self.assertEqual(debts[0], debts2[0])

    def test_without_outstanding_bills_none_paid(self):
        '''
        1. create 10 debts for an organization.
        2. creat a bill for the first debt
        3. create a bill for the second debt
        4. create 2 bills for the third debt
        5. Create 5 more debts
        There should only be 2 debts with upaid or under paid bills
        :return:
        '''
        profile = UserFactory.create()
        organization = OrganizationFactory.create(owner=profile)
        created_debts = MonthlyDebtFactory.create_batch(10, organization=organization)
        bills_created = created_debts[0].create_bills(1)
        created_debts[1].create_bills(1)
        created_debts[2].create_bills(2)
        MonthlyDebtFactory.create_batch(5)

        unpaid_debts_ids = Bill.objects.filter(Q(debt__organization=organization),
                                               Q(status=Bill.STATUS_UNPAID) | Q(status=Bill.STATUS_UNDER_PAID))
        unpaid_debts_ids = unpaid_debts_ids.distinct('debt').values('debt__pk')
        self.assertEqual(3, len(unpaid_debts_ids))
        debts = Debt.objects.filter(organization=organization).exclude(pk__in=unpaid_debts_ids)
        self.assertEqual(7, len(debts))



class TestPaymentFrequency(TestCase):

    def test_create(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create()
        self.assertEqual(1, PaymentFrequency.objects.count())
        i18n_results = [('en', 'Pay every month on'),
                        ('es', 'Pagar cada mes los')]
        for lang in i18n_results:
            translation.activate(lang[0])
            self.assertTrue(str(payment_frequency).startswith(lang[1]),
                            msg='%s does not start with %s' % (payment_frequency, lang[1]))

    def test_create_batch(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create_batch(5)
        self.assertEqual(5, PaymentFrequency.objects.count())

    def test_get_days_of_the_month(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create(frequency_values='2')
        day_list = payment_frequency.get_days_of_the_month()
        self.assertEqual(2, day_list[0])

    def test_get_days_of_the_month_2(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create(frequency_values='14,2')
        day_list = payment_frequency.get_days_of_the_month()
        self.assertEqual(2, day_list[0])
        self.assertEqual(2, len(day_list))

    def test_calculate_next_date(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create(frequency_values='15')
        ref_date = date(2015,11,28)
        next_date = payment_frequency.calculate_next_date(ref_date)
        self.assertEqual(date(2015,12,15), next_date)

    def test_calculate_next_date(self):
        payment_frequency = MonthlyPaymentFrequencyFactory.create(frequency_values='15,30')
        ref_date = date(2015,11,28)
        next_date = payment_frequency.calculate_next_date(ref_date)
        self.assertEqual(date(2015,11,30), next_date)


class TestBill(TestCase):

    def test_create(self):
        bill = MonthlyBillFactory.create()
        self.assertEqual(Bill.STATUS_UNPAID, bill.status)
        self.assertEqual(1, Bill.objects.count())

    def test_create_batch(self):
        bill = MonthlyBillFactory.create_batch(5)
        self.assertEqual(5, Bill.objects.count())

    def test_pay(self):
        bill = MonthlyBillFactory.create()
        payment = bill.pay()
        db_bill = Bill.objects.get(pk=bill.pk)
        self.assertEqual(payment.amount, db_bill.amount)
        self.assertEqual(db_bill.amount_paid(),payment.amount)
        self.assertEqual(Bill.STATUS_PAID, db_bill.status)

    def test_pay_twice(self):
        bill = MonthlyBillFactory.create()
        payment = bill.pay()
        self.assertEqual(payment.amount, bill.amount)
        self.assertIsNone(bill.pay())

        self.assertEqual(Bill.STATUS_PAID, bill.status)

    def test_pay_partial(self):
        bill = MonthlyBillFactory.create(amount=129.0)
        payment = bill.pay(amount=50.0)
        self.assertEqual(50.0, payment.amount)
        self.assertEqual(79.0, bill.amount_due())

        self.assertEqual(Bill.STATUS_UNDER_PAID, bill.status)

    def test_pay_partial_twice(self):
        bill = MonthlyBillFactory.create(amount=129.0)
        payment = bill.pay(amount=50.0)
        self.assertEqual(50.0, payment.amount)
        self.assertEqual(50.0, bill.amount_paid())

        self.assertEqual(79.0, bill.amount_due())
        bill.pay(amount=23.0)
        self.assertEqual(73.0, bill.amount_paid())

        self.assertEqual(Bill.STATUS_UNDER_PAID, bill.status)

    def test_get_unpaid(self):
        organization = OrganizationFactory.create()
        bills = MonthlyBillFactory.create_batch(5, debt__organization=organization)
        self.assertEqual(5, Bill.objects.get_unpaid(organization).count())
        self.assertEqual(bills[0].debt.organization, organization)
        bills[0].pay()
        self.assertEqual(4, Bill.objects.get_unpaid(organization).count())

    def test_paid(self):
        organization = OrganizationFactory.create()
        bills = MonthlyBillFactory.create_batch(5, debt__organization=organization)
        self.assertEqual(5, Bill.objects.get_unpaid(organization).count())
        self.assertEqual(bills[0].debt.organization, organization)
        bills[0].pay()
        bills[1].pay()
        self.assertEqual(2, Bill.objects.paid(organization).count())





