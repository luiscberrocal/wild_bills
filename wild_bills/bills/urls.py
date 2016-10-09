from django.conf.urls import url

from wild_bills.bills.views import DebtCreateView, DebtDetailView, DebtUpdateView, DebtListView, BillCreateView, BillListView, \
    BillDetailView, BillUpdateView, DebtDeleteView, \
    PaymentCreateView


urlpatterns = [
    #url(r'^profile/create/$', WildBillsProfileCreateView.as_view(), name='profile-create'),
    #url(r'^profile/(?P<pk>[\d]*)/update$', WildBillsProfileUpdateView.as_view(), name='profile-update'),
    url(r'^debt/$', DebtListView.as_view(), name='debt-list'),
    url(r'^debt/create/$', DebtCreateView.as_view(), name='debt-create'),
    url(r'^debt/(?P<pk>[\d]*)/$', DebtDetailView.as_view(), name='debt-detail'),
    url(r'^debt/(?P<pk>[\d]*)/update$', DebtUpdateView.as_view(), name='debt-update'),
    url(r'^debt/(?P<pk>[\d]*)/delete$', DebtDeleteView.as_view(), name='debt-delete'),
    url(r'^bill/$', BillListView.as_view(), name='bill-list'),
    url(r'^bill/paid/$', BillListView.as_view(), kwargs={'status': 'PAID'}, name='bill-list-paid'),
    url(r'^bill/create/$', BillCreateView.as_view(), name='bill-create'),
    url(r'^bill/(?P<pk>[\d]*)/$', BillDetailView.as_view(), name='bill-detail'),
    url(r'^bill/(?P<pk>[\d]*)/update$', BillUpdateView.as_view(), name='bill-update'),
    url(r'^payment/create/(?P<bill_pk>[\d]*)/$', PaymentCreateView.as_view(), name='payment-create'),
]
