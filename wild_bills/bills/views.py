

from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView, CreateView, DetailView, ListView, DeleteView
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ipware.ip import get_real_ip, get_ip

from .geoip import geo_ip_finder
from .utils import organization_manager
from .forms import DebtForm, BillForm, PaymentForm
from .models import Debt, Bill, Payment
import logging

logger = logging.getLogger(__name__)

class DebtViewMixin(object):

     def get(self, request, *args, **kwargs):
        debt_pk = int(kwargs['pk'])
        debt = Debt.objects.get(pk=debt_pk)
        if organization_manager.is_user_part_of_organization(self.request.user, debt.organization):
            return super(DebtViewMixin, self).get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(_('You cannot view a debt that is not part of your organization!'))


class DebtUpdateView(LoginRequiredMixin, UserFormKwargsMixin, DebtViewMixin, UpdateView):
    model = Debt
    context_object_name = 'debt'
    form_class = DebtForm

    def get_initial(self):
        data = dict()
        data['frequency_values'] = self.object.frequency.frequency_values
        data['frequency'] = self.object.frequency.frequency
        data['start_date'] = self.object.frequency.start_date
        return data


class DebtCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Debt
    form_class = DebtForm
    success_url = reverse_lazy('bills:debt-list')

    def get_initial(self):
        organization = organization_manager.get_selected_organization(self.request)
        data = {'organization': organization,
                'start_date': timezone.now().date()}
        return data

    def post(self, request, *args, **kwargs):
        if '_add_another' in request.POST:
            self.success_url = reverse('bills:debt-create')
        return super(DebtCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        msg = _('Debt to {payee} for {amount} was created').format(**form.cleaned_data)
        messages.success(self.request, msg)
        return super(DebtCreateView, self).form_valid(form)


class DebtDetailView(LoginRequiredMixin, UserFormKwargsMixin, DebtViewMixin, DetailView):
    model = Debt
    context_object_name = 'debt'


class DebtDeleteView(LoginRequiredMixin, UserFormKwargsMixin, DebtViewMixin, DeleteView):
    model = Debt
    success_url = reverse_lazy('bills:debt-list')


class DebtListView(LoginRequiredMixin, UserFormKwargsMixin, ListView):
    model = Debt
    context_object_name = 'debts'

    def get_queryset(self):
        qs = super(DebtListView, self).get_queryset()
        organization = organization_manager.get_selected_organization(self.request)
        return qs.filter(organization=organization)


class BillUpdateView(LoginRequiredMixin, UserFormKwargsMixin, UpdateView):
    model = Bill
    context_object_name = 'bill'
    form_class = BillForm


class BillCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Bill
    context_object_name = 'bill'
    form_class = BillForm


class BillDetailView(LoginRequiredMixin, DetailView):
    model = Bill
    context_object_name = 'bill'


class BillListView(LoginRequiredMixin, ListView):
    model = Bill
    context_object_name = 'bills'


    def get(self, request, *args, **kwargs):
        status = kwargs.get('status', None)
        if status == 'PAID':
            self.template_name = 'bills/paid_bill_list.html'
            self.paginate_by = 5
        return super(BillListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(BillListView, self).get_queryset()
        organization = organization_manager.get_selected_organization(self.request)
        status = self.kwargs.get('status', None)
        if status == 'PAID':
            qs = qs.filter(Q(debt__organization=organization), Q(status=Bill.STATUS_PAID) | Q(status=Bill.STATUS_OVER_PAID))
        else:
            debts_without_bills = Debt.objects.without_outstanding_bills(organization=organization)
            for debt in debts_without_bills:
                debt.create_bills(1)
            qs = qs.filter(Q(debt__organization=organization), Q(status=Bill.STATUS_UNPAID) | Q(status=Bill.STATUS_UNDER_PAID))
        return qs.order_by('due_date')




class PaymentCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    model = Payment
    context_object_name = 'payment'
    form_class = PaymentForm
    success_url = reverse_lazy('bills:bill-list')

    def get_initial(self):
        bill = Bill.objects.get(pk=self.kwargs['bill_pk'])
        data = {'bill': bill.pk,
                'amount': bill.amount,
                'date_paid': timezone.now().date(),
                'detail': _('Payment to {payee} for {amount}').format(payee=bill.debt.payee, amount= bill.amount)
                }
        return data
