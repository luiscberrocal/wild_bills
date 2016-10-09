# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0007_auto_20151214_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='debt',
            field=models.ForeignKey(to='bills.Debt', related_name='debts', verbose_name='Debt'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='due_date',
            field=models.DateField(verbose_name='Due date'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='payments',
            field=models.ManyToManyField(to='bills.Payment', related_name='bills', verbose_name='Payments'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='status',
            field=models.CharField(choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('UNDER_PAID', 'Under paid'), ('OVER_PAID', 'Over paid')], max_length=10, default='UNPAID', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='fixed_amount',
            field=models.BooleanField(default=False, verbose_name='Fixed amount'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='frequency',
            field=models.ForeignKey(to='bills.PaymentFrequency', verbose_name='Frequency'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='payee',
            field=models.CharField(max_length=150, verbose_name='Payee'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='display_name',
            field=models.CharField(help_text='Name that you communicate', max_length=150, verbose_name='Display name'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='legal_name',
            field=models.CharField(help_text='Official name. Only relevant if the organization is a company', max_length=150, blank=True, verbose_name='Legal name'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='organizations', blank=True, null=True, verbose_name='Members'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='owned_organizations', verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date_paid',
            field=models.DateField(default=datetime.date.today, verbose_name='Date paid'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='detail',
            field=models.CharField(max_length=255, null=True, blank=True, verbose_name='Detail'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='reference',
            field=models.CharField(max_length=255, null=True, blank=True, verbose_name='Reference'),
        ),
        migrations.AlterField(
            model_name='paymentfrequency',
            name='frequency',
            field=models.CharField(choices=[('Monthly', 'Monthly'), ('Weekly', 'Weekly'), ('Biweekly', 'Biweekly')], max_length=15, default='Monthly', verbose_name='Frequency'),
        ),
        migrations.AlterField(
            model_name='paymentfrequency',
            name='frequency_values',
            field=models.CharField(help_text='Which days of the month or days of the week the payment should occur. Values separated by comma', max_length=60, blank=True, verbose_name='Frequency values'),
        ),
        migrations.AlterField(
            model_name='paymentfrequency',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Start date'),
        ),
    ]
