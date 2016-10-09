import string
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from factory import LazyAttribute, lazy_attribute, SubFactory, Iterator
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from faker import Factory as FakerFactory

from ...users.tests.factories import UserFactory
from ..models import Organization, PaymentFrequency, Debt, Bill

__author__ = 'luiscberrocal'

faker = FakerFactory.create()


class OrganizationFactory(DjangoModelFactory):

    class Meta:
        model = Organization

    owner = SubFactory(UserFactory)

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











