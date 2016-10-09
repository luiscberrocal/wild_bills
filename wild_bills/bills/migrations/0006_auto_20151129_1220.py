# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_auto_20151127_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='object_id',
        ),
        migrations.AddField(
            model_name='bill',
            name='payments',
            field=models.ManyToManyField(related_name='bills', to='bills.Payment'),
        ),
    ]
