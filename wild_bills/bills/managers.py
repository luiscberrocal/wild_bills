
from django.db import models
from django.db.models import Q




class BillManager(models.Manager):

    def get_unpaid(self, organization):
        from .models import Bill
        return self.get_queryset().filter(Q(debt__organization=organization), Q(status=Bill.STATUS_UNPAID) | Q(status=Bill.STATUS_UNDER_PAID))

    def paid(self, organization):
        from .models import Bill
        return self.get_queryset().filter(Q(debt__organization=organization), Q(status=Bill.STATUS_PAID) | Q(status=Bill.STATUS_OVER_PAID))

class DebtManager(models.Manager):

    def without_outstanding_bills(self, organization):
        from .models import Bill
        unpaid_debts_ids = Bill.objects.filter(Q(debt__organization=organization),
                                               Q(status=Bill.STATUS_UNPAID) | Q(status=Bill.STATUS_UNDER_PAID))
        unpaid_debts_ids = unpaid_debts_ids.distinct('debt').values('debt__pk')
        return self.get_queryset().filter(organization=organization).exclude(pk__in=unpaid_debts_ids)