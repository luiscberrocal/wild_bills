from braces.forms import UserKwargModelFormMixin
from django import forms

from .utils import organization_manager
from .models import Debt, PaymentFrequency, Bill, WildBillsProfile, Organization, Payment
from django.utils.translation import ugettext_lazy as _


class PaymentFrequencyForm(forms.ModelForm):
    class Meta:
        model = PaymentFrequency
        fields = ['frequency_values', 'frequency', 'start_date']


class DebtForm(UserKwargModelFormMixin, forms.ModelForm):
    frequency = forms.ChoiceField(choices=PaymentFrequency.FREQ_CHOICES, label=_('Frequency'))
    frequency_values = forms.CharField(required=True, label=_('Values'),
                                       help_text=_('Days of the month separated by commas'))
    start_date = forms.DateField(required=False, label=_('Start date'))

    def __init__(self, *args, **kwargs):
        super(DebtForm, self).__init__(*args, **kwargs)
        self.fields['organization'].queryset = organization_manager.get_user_organizations(self.user)
        if len(organization_manager.get_user_organizations(self.user)) == 1:
            self.fields['organization'].widget = forms.HiddenInput()

    class Meta:
        model = Debt  # , 'frequency',
        fields = ['payee', 'description', 'amount', 'fixed_amount', 'organization', 'end_date', 'category']

    def clean_organization(self):
        organization = self.cleaned_data['organization']
        orgas = organization_manager.get_user_organizations(self.user)
        if organization in orgas:
            return organization
        else:
            raise forms.ValidationError(_('You cannot modify a Debt if '
                                          'you do not own it or are a '
                                          'member of the organization'))

    def save(self, commit=True):
        debt = super(DebtForm, self).save(commit=False)
        payment_frequency = PaymentFrequency(frequency=self.cleaned_data['frequency'],
                                             frequency_values=self.cleaned_data['frequency_values'],
                                             start_date=self.cleaned_data['start_date'])

        payment_frequency.save()
        debt.frequency = payment_frequency
        if commit:
            debt.save()
        return debt


class BillForm(forms.ModelForm):

    class Meta:
        model = Bill
        fields = ['debt', 'amount', 'due_date']


class WildBillsProfileForm(forms.ModelForm):

    password1 = forms.CharField(required=False, label=_('Password'))
    password2 = forms.CharField(required=False, label=_('Repeat password'))

    update = False

    class Meta:
        model = WildBillsProfile
        fields = ['username', 'email', 'last_name', 'first_name', 'country' ]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        elif password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        elif not self.instance.pk:
            raise forms.ValidationError(_("Pasword is required"))
        return password2

    def save(self, commit=True):
        wbprofile = super(WildBillsProfileForm, self).save(commit=commit)
        if commit:
            if self.cleaned_data.get('password2'):
                wbprofile.set_password(self.cleaned_data.get('password2'))
                wbprofile.save()
            user_organizations = organization_manager.get_user_organizations(wbprofile)
            if len(user_organizations) == 0:
                org_name = _('%s Family') % (wbprofile.last_name)
                Organization.objects.create(display_name=org_name, owner=wbprofile)
        return wbprofile


class PaymentForm(UserKwargModelFormMixin, forms.ModelForm):

    bill = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.bill_object = None

    class Meta:
        model = Payment
        fields = ('amount', 'detail', 'date_paid', 'reference')

    def clean_bill(self):
        try:
            bill_pk = self.cleaned_data.get('bill')
            self.bill_object = Bill.objects.get(pk=bill_pk)
        except Bill.DoesNotExist:
            raise forms.ValidationError('There is no bill with pk %d' % bill_pk)

    def save(self, commit=True):
        payment = super(PaymentForm, self).save(commit=commit)
        if commit:
            self.bill_object.payments.add(payment)
            self.bill_object.set_status()
            self.bill_object.save()
        return payment




