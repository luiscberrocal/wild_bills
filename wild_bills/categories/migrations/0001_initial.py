# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_public', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL, related_name='owned_categories', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('language_code', models.CharField(verbose_name='Language', max_length=15, db_index=True)),
                ('name', models.CharField(verbose_name='Name', max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
                ('master', models.ForeignKey(to='categories.Category', related_name='translations', editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Category Translation',
                'default_permissions': (),
                'managed': True,
                'db_tablespace': '',
                'db_table': 'categories_category_translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
