# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('payee', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fixed_amount', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentFrequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('day_of_the_month', models.CharField(help_text='Which days of the month the payment should occur. Values separated by comma', blank=True, max_length=15)),
                ('day_of_the_week', models.CharField(blank=True, max_length=3)),
                ('frequency', models.CharField(choices=[('Specic Days', 'Specic Days'), ('Weekly', 'Weekly'), ('Biweekly', 'Biweekly')], max_length=15)),
                ('start_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='debt',
            name='frequency',
            field=models.ForeignKey(to='bills.PaymentFrequency'),
        ),
        migrations.AddField(
            model_name='debt',
            name='organization',
            field=models.ForeignKey(related_name='debts', to='bills.Organization'),
        ),
    ]
