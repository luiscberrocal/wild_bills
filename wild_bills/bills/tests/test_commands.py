from django.core.management import call_command
from django.test import TestCase

from ...users.tests.factories import UserFactory
from ..models import Bill
from .factories import  OrganizationFactory, MonthlyDebtFactory


class CommandsTestCase(TestCase):

    def setUp(self):
        # self.client = Client()
        self.username = 'obiwan'
        self.password = 'password'
        self.profile = UserFactory.create(username=self.username,
                                                      password=self.password,
                                                      email='obiwan@jedi.org')
        self.organization = OrganizationFactory.create(owner=self.profile)

    def test_create_bills(self):
        " Test my create_bills"
        MonthlyDebtFactory.create_batch(5, organization=self.organization)
        self.assertEqual(0, Bill.objects.count())
        args = [self.username,]
        opts = {}
        call_command('create_bills', *args, **opts)
        self.assertEqual(5, Bill.objects.count())
