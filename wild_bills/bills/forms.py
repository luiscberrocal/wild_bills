from braces.forms import UserKwargModelFormMixin
from django import forms

from .utils import organization_manager
from .models import Debt, PaymentFrequency, Bill, Organization, Payment
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




