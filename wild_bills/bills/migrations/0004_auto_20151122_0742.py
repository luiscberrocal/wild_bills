# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_auto_20151121_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=0, verbose_name='Amount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentfrequency',
            name='frequency',
            field=models.CharField(default='Monthly', choices=[('Monthly', 'Monthly'), ('Weekly', 'Weekly'), ('Biweekly', 'Biweekly')], max_length=15),
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together=set([('debt', 'due_date')]),
        ),
    ]
