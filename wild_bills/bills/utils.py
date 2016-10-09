import calendar
from datetime import date, datetime

from delorean import Delorean
from django.db.models import Q

from django.conf import settings


class OrganizationManager(object):
    selected_organization_key = 'selected_organization_pk'

    def get_user_organizations(self, user):
        # To avoid circular imports
        from .models import Organization

        orgas = (Organization.objects
            .filter(Q(members=user) | Q(owner=user))
            .distinct())
        return orgas

    def is_user_part_of_organization(self, user, organization):
        return organization in self.get_user_organizations(user)

    def set_selected_organization(self, request, organization):
        key = self.selected_organization_key
        request.session[key] = organization.pk

    def get_selected_organization(self, request):
        key = self.selected_organization_key
        if key not in request.session:
            return

        # To avoid circular imports
        from .models import Organization

        pk = request.session[key]
        organization = Organization.objects.get(pk=pk)
        return organization


organization_manager = OrganizationManager()


class FrequencyCalculator(object):

    def __init__(self, time_zone=None):
        self.days_of_week = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
        if time_zone is None:
            self.time_zone = settings.TIME_ZONE
        else:
            self.time_zone = time_zone

    def get_next_week_date(self, previous_date, day_of_week):
        if day_of_week not in self.days_of_week:
            raise ValueError('%s is not a valid week day' % day_of_week)
        d = self._get_delorean(previous_date)
        #return d.next_saturday()
        method_name = 'next_%s' % day_of_week
        return getattr(d, method_name)().date

    def get_next_month_date(self, previous_date):
        d = self._get_delorean(previous_date)
        #return d.next_saturday()
        method_name = 'next_month'
        return getattr(d, method_name)().date

    def _get_delorean(self, ref_date):
        if isinstance(ref_date, date):
            ref_date = datetime.combine(ref_date, datetime.min.time())
        d = Delorean(ref_date, self.time_zone)
        return d

    def _build_deloreans(self, ref_date, days_list):
        deloreans = list()
        for day in days_list:
            last_day = calendar.monthrange(ref_date.year, ref_date.month)[1]
            if day > last_day:
                day = last_day
            cdate = date(ref_date.year, ref_date.month, day)
            deloreans.append(self._get_delorean(cdate))
        return deloreans

    def get_next_closest(self, ref_date, days_list):
        next_date = None
        ref_delorean = self._get_delorean(ref_date)
        deloreans = self._build_deloreans(ref_date, days_list)
        count = 0
        for day in deloreans:
            if ref_delorean < day:
                next_date = day.date
                break
            elif ref_delorean == day:
                if len(deloreans) == 1:
                    next_date = day.next_month().date
                    break
                elif count + 1 == len(deloreans):
                    next_date = deloreans[count - 1].next_month().date
                    break
                else:
                    next_date = deloreans[count + 1].date
                    break
            elif ref_delorean > day:
                if len(deloreans) == 1:
                    next_date = day.next_month().date
                    break
                elif count + 1 == len(deloreans):
                    next_date = deloreans[count - 1].next_month.date
                    break
            count += 1

        return next_date


frequency_calculator = FrequencyCalculator()
