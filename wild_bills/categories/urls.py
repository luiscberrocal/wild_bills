from django.conf.urls import patterns, url

from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='category-list'),
    # url(r'^/create/$', CategoryCreateView.as_view(), name='category-create'),
    url(r'^(?P<slug>[\w-]*)/$', CategoryDetailView.as_view(), name='category-detail'),
    # url(r'^/(?P<pk>[\d]*)/update$', CategoryUpdateView.as_view(), name='category-update'),
]
