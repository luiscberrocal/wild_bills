from django.forms import model_to_dict
from django.test import TestCase
from django.utils import translation, timezone

from ...categories.tests.factories import category_factory
from ..forms import DebtForm, PaymentForm
from ..models import PaymentFrequency, Organization, Bill
from .mixins import UserSetupMixin
from .factories import OrganizationFactory, MonthlyDebtFactory


class TestDebtForm(TestCase):

    def test_valid_data(self):
        organization = OrganizationFactory.create()
        data = {'payee': 'Bank of America',
                'description': 'Car',
                'amount': 123.40,
                'fixed_amount': False,
                'organization': organization.pk,
                'frequency': PaymentFrequency.FREQ_MONTHLY,
                'frequency_values': '15, 30'}

        form = DebtForm(data)
        self.assertTrue(form.is_valid())
        debt = form.save()
        self.assertEqual(data['payee'], debt.payee)

    def test_valid_with_category(self):
        organization = OrganizationFactory.create()
        category = category_factory.create_defaults()[0]
        data = {'payee': 'Bank of America',
                'description': 'Car',
                'amount': 123.40,
                'fixed_amount': False,
                'organization': organization.pk,
                'frequency': PaymentFrequency.FREQ_MONTHLY,
                'frequency_values': '15, 30',
                'category': category.pk}

        form = DebtForm(data)
        self.assertTrue(form.is_valid())
        debt = form.save()
        self.assertEqual(data['payee'], debt.payee)
        self.assertEqual(data['category'], debt.category.pk)


class TestPaymentForm(TestCase):

    def test_create_payment(self):
        debt = MonthlyDebtFactory.create(amount=100.0)
        bill = debt.create_bills(1)[0]
        data = { 'amount': debt.amount,
                 'detail': 'Payment to %s' % debt.payee,
                 'date_paid': timezone.now().date(),
                 'reference': 'PAID',
                 'bill': bill.pk}
        form = PaymentForm(data)
        self.assertTrue(form.is_valid())
        payment  = form.save()
        self.assertEqual(data['amount'], payment.amount)
        self.assertEqual(0.0, bill.amount_due())
        bill = Bill.objects.get(pk=bill.pk)
        self.assertEqual(Bill.STATUS_PAID, bill.status)


# class TestWildBillsProfileForm(UserSetupMixin, TestCase):
#
#     def test_valid_data(self):
#         form = UserForm(self.profile_dict)
#         self.assertTrue(form.is_valid())
#         profile = form.save()
#         self.assertEqual(self.profile_dict['username'], profile.username)
#
#         i18n_results = ['en', 'Parker Family']
#
#         translation.activate(i18n_results[0])
#         organization = Organization.objects.get(owner=profile)
#         self.assertEqual(i18n_results[1], organization.display_name)
#         login = self.client.login(username=self.profile_dict['username'],
#                                   password=self.profile_dict['password1'])
#         self.assertTrue(login)
#
#     def test_valid_data_es(self):
#         i18n_results = ['es', 'Familia Parker']
#
#         translation.activate(i18n_results[0])
#         form = WildBillsProfileForm(self.profile_dict)
#         self.assertTrue(form.is_valid())
#         profile = form.save()
#         self.assertEqual(self.profile_dict['username'], profile.username)
#
#         organization = Organization.objects.get(owner=profile)
#         self.assertEqual(i18n_results[1], organization.display_name)
#         login = self.client.login(username=self.profile_dict['username'],
#                                   password=self.profile_dict['password1'])
#         self.assertTrue(login)
#
#     def test_valid_blank_passwords(self):
#         self.profile_dict['password1'] = ''
#         self.profile_dict['password2'] = ''
#         i18n_results = [('en', 'Pasword is required'),
#                         ('es', 'La contraseña es requerida')]
#         for lang in i18n_results:
#             translation.activate(lang[0])
#             form = WildBillsProfileForm(self.profile_dict)
#             self.assertFalse(form.is_valid())
#             self.assertEqual(lang[1], form.errors['password2'][0])
#             login = self.client.login(username=self.profile_dict['username'],
#                                       password=self.profile_dict['password1'])
#             self.assertFalse(login)
#
#     def test_one_password_blank(self):
#         i18n_results = [('en', 'The two password fields didn\'t match.'),
#                         ('es', 'Las dos contraseñas no son iguales.')]
#         for lang in i18n_results:
#             translation.activate(lang[0])
#             self.profile_dict['password2'] = ''
#             form = WildBillsProfileForm(self.profile_dict)
#             self.assertFalse(form.is_valid())
#             self.assertEqual(lang[1], form.errors['password2'][0])
#             login = self.client.login(username=self.profile_dict['username'],
#                                       password=self.profile_dict['password1'])
#             self.assertFalse(login)
#
#     def test_update_data(self):
#         wbprofile = WildBillsProfileFactory.create()
#         data = model_to_dict(wbprofile)
#         data['username'] = 'spiderman'
#         data['password1'] = 'tiger'
#         data['password2'] = 'tiger'
#         form = WildBillsProfileForm(data, instance=wbprofile)
#         profile = form.save()
#         self.assertEqual(data['username'], profile.username)
#         login = self.client.login(username=data['username'],
#                                   password=data['password1'])
#         self.assertTrue(login)
#
#     def test_update_data_blank_passwords(self):
#         wbprofile = WildBillsProfileFactory.create(password='thunder')
#         data = model_to_dict(wbprofile)
#         data['username'] = 'spiderman'
#         data['password1'] = ''
#         data['password2'] = ''
#         form = WildBillsProfileForm(data, instance=wbprofile)
#         profile = form.save()
#         self.assertEqual(data['username'], profile.username)
#         login = self.client.login(username=data['username'],
#                                   password='thunder')
#         self.assertTrue(login)
#
#     def test_different_passwords(self):
#         self.profile_dict['password1'] = 'kilo'
#         self.profile_dict['password2'] = 'kilo2'
#         i18n_results = [('en', 'The two password fields didn\'t match.'),
#                         ('es', 'Las dos contraseñas no son iguales.')]
#         for lang in i18n_results:
#             translation.activate(lang[0])
#             form = WildBillsProfileForm(self.profile_dict)
#             self.assertFalse(form.is_valid())
#             self.assertEqual(lang[1], form.errors['password2'][0])
