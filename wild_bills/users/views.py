# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


# class WildBillsProfileCreateView(CreateView):
#
#     model = WildBillsProfile
#     context_object_name = 'wbprofile'
#     form_class = WildBillsProfileForm
#     success_url = '/'
#
#     def get_initial(self):
#         ip = get_ip(self.request)
#         logger.debug('Client IP: %s' % ip)
#         country_code = geo_ip_finder.get_country_code(ip)
#         logger.debug('Client country: %s' % country_code)
#         if country_code == 'XX':
#             logger.warn('Had to coerce country to Panama')
#             country_code = 'PA'
#         data = {'country': country_code}
#         return data
#
#
# class WildBillsProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = WildBillsProfile
#     context_object_name = 'wbprofile'
#     form_class = WildBillsProfileForm
#     success_url = '/'
#
#     def get(self, request, *args, **kwargs):
#         if request.user.pk:
#             if request.user.pk != int(kwargs['pk']):
#                 return HttpResponseForbidden(_('You cannot modify other profiles but your own!!'))
#         return super(WildBillsProfileUpdateView, self).get(request, *args, **kwargs)
