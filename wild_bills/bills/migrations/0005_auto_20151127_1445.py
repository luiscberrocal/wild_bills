# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_auto_20151122_0742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentfrequency',
            name='day_of_the_month',
        ),
        migrations.RemoveField(
            model_name='paymentfrequency',
            name='day_of_the_week',
        ),
        migrations.AddField(
            model_name='paymentfrequency',
            name='frequency_values',
            field=models.CharField(help_text='Which days of the month or days of the week the payment should occur. Values separated by comma', blank=True, max_length=60),
        ),
    ]
