from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.test import override_settings, TestCase
from django.utils import translation, timezone
from with_asserts.mixin import AssertHTMLMixin

from ...users.tests.factories import UserFactory
from ..models import Debt, Bill
from .factories import MonthlyDebtFactory, OrganizationFactory, \
    MonthlyPaymentFrequencyFactory
import logging

from .mixins import UserSetupMixin

logger = logging.getLogger(__name__)


class TestDebtViews(AssertHTMLMixin, UserSetupMixin, TestCase):

    def test_access_create_view_get(self):
        organization = OrganizationFactory.create(owner=self.profile)
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse('bills:debt-create'))
        self.assertEqual(response.status_code, 200)
        OrganizationFactory.create_batch(2)
        # Check that there are only organizations available that the user is part of
        # with self.assertHTML(response, 'select#id_organization option') as elems:
        #     self.assertEqual(2, len(elems))
        # verify if start date is today
        today = timezone.now().date().strftime('%Y-%m-%d')
        with self.assertHTML(response, 'input#id_start_date') as (elem,):
            self.assertEqual(today, elem.value)

        with self.assertHTML(response, 'div.container h1') as (elem,):
            self.assertEqual('Add a new debt', elem.text.strip())
        with self.assertHTML(response, 'a#cancel-btn') as (elem,):
            self.assertEqual(reverse('bills:debt-list'), elem.attrib['href'])
        #Verify that organization is hidden since user has only one organization
        with self.assertHTML(response, 'input#id_organization') as (elem,):
            self.assertEqual('hidden', elem.attrib['type'])

    def test_create_view_get_2_organizations(self):
        OrganizationFactory.create(owner=self.profile)
        organization = OrganizationFactory.create(owner=self.profile, display_name='Business Kenobi')
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse('bills:debt-create'))
        self.assertEqual(response.status_code, 200)
        OrganizationFactory.create_batch(2)
        # Check that there are only organizations available that the user is part of
        with self.assertHTML(response, 'select#id_organization option') as elems:
            self.assertEqual(3, len(elems))
            self.assertEqual(organization.display_name, elems[1].text)



    def _get_debt_data(self, add_another=False):
        organization = OrganizationFactory.create(owner=self.profile)
        data = {'payee': 'Stan Lee',
                'description': 'IOU to Stan Lee',
                'amount': Decimal(145.00),
                'fixed_amount': True,
                'organization': organization.pk,
                'frequency': 'Monthly',
                'frequency_values': '15',
                'start_date': timezone.now().date()
                }
        if add_another:
            data['_add_another'] = 'Save and add another'
        return data


    def test_access_create_view_post(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        frequency = MonthlyPaymentFrequencyFactory.create()
        data = self._get_debt_data()
        response = self.client.post(reverse('bills:debt-create'), data=data)
        self.assertEqual(response.status_code, 302)
        url = '/%s/bills/debt/' % ('en')
        self.assertEqual(response.url, url)
        self.assertEqual(1, Debt.objects.count())

    def test_create_view_post_add_another(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)

        data = self._get_debt_data(add_another=True)
        response = self.client.post(reverse('bills:debt-create'), data=data)
        self.assertEqual(response.status_code, 302)
        url = '/%s/bills/debt/create/' % ('en')
        self.assertEqual(response.url, url)
        self.assertEqual(1, Debt.objects.count())

    def test_create_view_post_add_another_message(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        frequency = MonthlyPaymentFrequencyFactory.create()
        data = self._get_debt_data(add_another=True)
        response = self.client.post(reverse('bills:debt-create'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, Debt.objects.count())
        with self.assertHTML(response, 'div.alert.alert-success div.container ul li') as (elems):
            self.assertEqual(1, len(elems))


    def test_access_denied_create_view(self):
        i18_langs = ['es', 'en']
        for lang in i18_langs:
            translation.activate(lang)
            response = self.client.get(reverse('bills:debt-create'))
            self.assertEqual(response.status_code, 302)
            url = '/{0}/accounts/login/?next=/{0}/bills/debt/create/'.format(lang)
            self.assertEqual(response.url, url)

    def test_access_detail_view(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        organization = OrganizationFactory.create(owner=self.profile)
        debt = MonthlyDebtFactory.create(organization=organization)
        response = self.client.get(reverse('bills:debt-detail', kwargs={'pk': debt.pk}))
        self.assertEqual(response.status_code, 200)
        with self.assertHTML(response, 'div#id_payee') as (elem,):
            self.assertEqual(str(debt.payee), elem.text.strip())

    def test_access_denied_detail_view(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        organization = OrganizationFactory.create()
        debt = MonthlyDebtFactory.create(organization=organization)
        response = self.client.get(reverse('bills:debt-detail', kwargs={'pk': debt.pk}))
        self.assertEqual(response.status_code, 403)

    def test_access_update_view(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        organization = OrganizationFactory.create(owner=self.profile)
        debt = MonthlyDebtFactory.create(organization=organization)
        response = self.client.get(reverse('bills:debt-update', kwargs={'pk': debt.pk}))
        self.assertEqual(response.status_code, 200)
        with self.assertHTML(response, 'div.container h1') as (elem,):
            self.assertEqual('Editing debt to %s' % debt.payee, elem.text.strip())
        with self.assertHTML(response, 'a#cancel-btn') as (elem,):
            self.assertEqual(reverse('bills:debt-detail', kwargs={'pk': debt.pk}), elem.attrib['href'])
            # html body div.container form div.row div.col-md-12 a.btn.btn-primary

    def test_delete_view(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        organization = OrganizationFactory.create(owner=self.profile)
        debt = MonthlyDebtFactory.create(organization=organization)
        debt_dict = model_to_dict(debt)
        response = self.client.get(reverse('bills:debt-delete', kwargs={'pk': debt.pk}))
        self.assertEqual(response.status_code, 200)
        with self.assertHTML(response, 'p#delete-confirm-message') as (elem,):
            self.assertEqual('Are you sure you want to delete debt to "%s"?' % debt.payee, elem.text.strip())
            # response = self.client.post(reverse('bills:debt-delete'), kwargs={'pk': debt.pk})
            # self.assertEqual(response.status_code, 200)

    def test_access_denied_update_view(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        debt = MonthlyDebtFactory.create()
        response = self.client.get(reverse('bills:debt-update', kwargs={'pk': debt.pk}))
        self.assertEqual(response.status_code, 403)

    def test_access_list_view(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        organization = OrganizationFactory.create(owner=self.profile)
        MonthlyDebtFactory.create_batch(10, organization=organization)
        MonthlyDebtFactory.create_batch(5)

        response = self.client.get(reverse('bills:debt-list'))
        self.assertEqual(response.status_code, 200)
        with self.assertHTML(response, 'tbody tr.row') as elems:
            self.assertEqual(10, len(elems))


class TestBillViews(AssertHTMLMixin, UserSetupMixin, TestCase):

    def _create_debts_and_bills(self, organization_debts=10, other_debts=5, pay_first_n_bills=0):
        organization = OrganizationFactory.create(owner=self.profile)
        MonthlyDebtFactory.create_batch(10, organization=organization)
        MonthlyDebtFactory.create_batch(5)
        for debt in Debt.objects.all():
            debt.create_bills(1)
        if pay_first_n_bills:
            bills = Bill.objects.filter(debt__organization=organization)[:pay_first_n_bills]
            for bill in bills:
                bill.pay()
            paid_bills = Bill.objects.paid(organization).order_by('due_date')
            self.assertEqual(pay_first_n_bills, len(paid_bills))
        return organization

    def test_bill_list(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        self._create_debts_and_bills()

        response = self.client.get(reverse('bills:bill-list'))
        self.assertEqual(response.status_code, 200)
        with self.assertHTML(response, 'tbody tr.row') as elems:
            self.assertEqual(10, len(elems))

    def test_bill_list_paid(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)

        self._create_debts_and_bills(pay_first_n_bills=5)
        response = self.client.get(reverse('bills:bill-list-paid'))
        self.assertEqual(response.status_code, 200)
        with self.assertHTML(response, 'tbody tr.row') as elems:
            self.assertEqual(5, len(elems))

    def test_bill_list_paid_pagination(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        self._create_debts_and_bills(pay_first_n_bills=7)

        response = self.client.get(reverse('bills:bill-list-paid'))
        self.assertEqual(response.status_code, 200)

        with self.assertHTML(response, 'tbody tr.row') as elems:
            self.assertEqual(5, len(elems))
        #html body div.container table.table tfoot tr.row td nav ul.pagination
        with self.assertHTML(response, 'td nav ul.pagination li') as elems:
            self.assertEqual(4, len(elems))

    def test_access_list_view_some_paid(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        organization = self._create_debts_and_bills()
        unpaid_bills = Bill.objects.filter(debt__organization=organization, status=Bill.STATUS_UNPAID).count()
        self.assertEqual(10, unpaid_bills)
        response = self.client.get(reverse('bills:bill-list'))
        with self.assertHTML(response, 'tbody tr.row') as elems:
            self.assertEqual(10, len(elems))
        bill = Bill.objects.filter(debt__organization=organization, status=Bill.STATUS_UNPAID)[0]
        with self.assertHTML(response, 'tr.row td#due-date-%s' % bill.pk) as (elems,):
            self.assertEqual(bill.due_date.strftime('%b. %-d, %Y'), elems.text.strip())
        bill.pay()
        unpaid_bills = Bill.objects.filter(debt__organization=organization, status=Bill.STATUS_UNPAID).count()
        self.assertEqual(9, unpaid_bills)
        #bill.save()
        response = self.client.get(reverse('bills:bill-list'))
        self.assertEqual(response.status_code, 200)
        #html body div.container table.table tbody tr.row td#due-date-23.col-md-2

        self.assertNotHTML(response, 'tr.row td#due-date-%s' % bill.pk)


# class TestWildBillsProfileViews(UserSetupMixin, AssertHTMLMixin, TestCase):
#     def test_create_profile_one_password_different(self):
#         response = self.client.get(reverse('bills:profile-create'))
#         self.assertEqual(response.status_code, 200)
#         self.profile_dict['password2'] = 'poli'
#         i18n_results = [('en', "The two password fields didn't match."),
#                         ('es', 'Las dos contraseñas no son iguales.')]
#         for lang in i18n_results:
#             translation.activate(lang[0])
#             response = self.client.post(reverse('bills:profile-create'), data=self.profile_dict)
#             self.assertEqual(response.status_code, 200)
#             with self.assertHTML(response, 'div.has-error div.help-block') as (elem,):
#                 self.assertEqual(lang[1], elem.text.strip())
#
#     def test_create_profile_password2_blank(self):
#         response = self.client.get(reverse('bills:profile-create'))
#         self.assertEqual(response.status_code, 200)
#         self.profile_dict['password2'] = ''
#         i18n_results = [('en', "The two password fields didn't match."),
#                         ('es', 'Las dos contraseñas no son iguales.')]
#         for lang in i18n_results:
#             translation.activate(lang[0])
#             response = self.client.post(reverse('bills:profile-create'), data=self.profile_dict)
#             self.assertEqual(response.status_code, 200)
#             with self.assertHTML(response, 'div.has-error div.help-block') as (elem,):
#                 self.assertEqual(lang[1], elem.text.strip())
#
#     def test_create_profile_password1_blank(self):
#         response = self.client.get(reverse('bills:profile-create'))
#         self.assertEqual(response.status_code, 200)
#         self.profile_dict['password1'] = ''
#         i18n_results = [('en', "The two password fields didn't match."),
#                         ('es', 'Las dos contraseñas no son iguales.')]
#         for lang in i18n_results:
#             translation.activate(lang[0])
#             response = self.client.post(reverse('bills:profile-create'), data=self.profile_dict)
#             self.assertEqual(response.status_code, 200)
#             with self.assertHTML(response, 'div.has-error div.help-block') as (elem,):
#                 self.assertEqual(lang[1], elem.text.strip())
#
#     def test_create_profile(self):
#         response = self.client.get(reverse('bills:profile-create'))
#         self.assertEqual(response.status_code, 200)
#         response = self.client.post(reverse('bills:profile-create'), data=self.profile_dict)
#         self.assertEqual(response.status_code, 302)
#         created_profile = User.objects.get(username=self.profile_dict['username'])
#         self.assertIsNotNone(created_profile)
#
#     def test_update_profile(self):
#         login = self.client.login(username=self.username,
#                                   password=self.password)
#         self.assertTrue(login)
#         response = self.client.get(reverse('bills:profile-update', kwargs={'pk': self.profile.pk}))
#         self.assertEqual(response.status_code, 200)
#         with self.assertHTML(response, 'input[id="id_username"]') as (elem,):
#             self.assertEqual(self.username, elem.value)
#         profile_dict = model_to_dict(self.profile)
#         profile_dict['country'] = 'US'
#         response = self.client.post(reverse('bills:profile-update', kwargs={'pk': self.profile.pk}), data=profile_dict)
#         self.assertEqual(response.status_code, 302)
#
#         updated_profile = User.objects.get(pk=self.profile.pk)
#         self.assertEqual('US', updated_profile.country.code)
#
#     def test_update_profile_permission_denied(self):
#         other_profile = UserFactory.create()
#         login = self.client.login(username=self.username,
#                                   password=self.password)
#         self.assertTrue(login)
#         response = self.client.get(reverse('bills:profile-update', kwargs={'pk': other_profile.pk}))
#         self.assertEqual(response.status_code, 403)


class TestHomePageView(UserSetupMixin, AssertHTMLMixin, TestCase):
    def test_no_login_i18n(self):
        i18n_results = [('es', 'Registrarse'), ('en', 'Sign up')]
        for lang in i18n_results:
            translation.activate(lang[0])
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)
            with self.assertHTML(response, 'a[id="signup-btn"]') as (elem,):
                self.assertEqual(lang[1], elem.text)

    def test_login(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotHTML(response, 'a[id="signup-btn"]')


class TestPaymentCreateView(UserSetupMixin, AssertHTMLMixin, TestCase):

    def test_create_payment(self):
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertTrue(login)
        organization = OrganizationFactory.create(owner=self.profile)
        debt = MonthlyDebtFactory.create(organization=organization)
        bill = debt.create_bills(1)[0]
        response = self.client.get(reverse('bills:payment-create', kwargs={'bill_pk': bill.pk}))
        self.assertEqual(response.status_code, 200)
        with self.assertHTML(response, 'input#id_bill') as (elem,):
            self.assertEqual(bill.pk, int(elem.attrib['value'].strip()))
        payment_dict = {'amount': debt.amount,
                        'detail': 'Payment to %s' % debt.payee,
                        'date_paid': timezone.now().date(),
                        'reference': 'PAID',
                        'bill': bill.pk}
        response = self.client.post(reverse('bills:payment-create',
                                            kwargs={'bill_pk': bill.pk}),
                                    data=payment_dict)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(0.0, bill.amount_due())
        bill = Bill.objects.get(pk=bill.pk)
        self.assertEqual(Bill.STATUS_PAID, bill.status)

        #html body div.container form div.tab-content div#project-info.tab-pane.active div.form-group input#id_bill.form-control
