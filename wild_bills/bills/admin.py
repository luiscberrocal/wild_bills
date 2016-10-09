from django.contrib import admin

# Register your models here.
from .models import  Organization, PaymentFrequency, Debt, Bill, Payment


class PaymentFrequencyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'frequency_values', 'frequency', 'start_date']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'display_name', 'legal_name', 'owner')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(PaymentFrequency, PaymentFrequencyAdmin)
admin.site.register(Debt)
admin.site.register(Bill)
admin.site.register(Payment)
