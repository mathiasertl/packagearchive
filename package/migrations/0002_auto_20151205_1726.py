# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-05 16:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='components',
        ),
        migrations.DeleteModel(
            name='Package',
        ),
    ]
