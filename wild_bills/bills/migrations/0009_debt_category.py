# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('bills', '0008_auto_20151226_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='debt',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='categories.Category', related_name='debts', blank=True, null=True),
        ),
    ]
