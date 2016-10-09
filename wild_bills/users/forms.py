from django import forms

from ..bills.models import Organization
from ..bills.utils import organization_manager
from .models import User
from django.utils.translation import ugettext_lazy as _

class WildBillsSignUpForm(forms.ModelForm):

    password1 = forms.CharField(required=False, label=_('Password'))
    password2 = forms.CharField(required=False, label=_('Repeat password'))

    update = False

    class Meta:
        model = User
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

    # def save(self, commit=True):
    #     wbprofile = super(WildBillsSignUpForm, self).save(commit=commit)
    #     if commit:
    #         if self.cleaned_data.get('password2'):
    #             wbprofile.set_password(self.cleaned_data.get('password2'))
    #             wbprofile.save()
    #         user_organizations = organization_manager.get_user_organizations(wbprofile)
    #         if len(user_organizations) == 0:
    #             org_name = _('%s Family') % (wbprofile.last_name)
    #             Organization.objects.create(display_name=org_name, owner=wbprofile)
    #     return wbprofile

    def signup(self, request, user):
        if self.cleaned_data.get('password2'):
            user.set_password(self.cleaned_data.get('password2'))
            user.save()
        user_organizations = organization_manager.get_user_organizations(user)
        if len(user_organizations) == 0:
            org_name = _('%s Family') % (user.last_name)
            Organization.objects.create(display_name=org_name, owner=user)

