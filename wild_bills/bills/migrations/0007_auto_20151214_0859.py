# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0006_auto_20151129_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='status',
            field=models.CharField(choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('UNDER_PAID', 'Under paid'), ('OVER_PAID', 'Over paid')], default='UNPAID', max_length=10),
        ),
        migrations.AlterField(
            model_name='debt',
            name='organization',
            field=models.ForeignKey(to='bills.Organization', verbose_name='Organization', related_name='debts'),
        ),
        migrations.AlterField(
            model_name='wildbillsprofile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='Country'),
        ),
    ]
