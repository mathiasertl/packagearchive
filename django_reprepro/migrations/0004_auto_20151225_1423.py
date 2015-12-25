# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_reprepro', '0003_auto_20151225_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('version', models.CharField(max_length=32)),
                ('arch', models.CharField(max_length=8)),
                ('components', models.ManyToManyField(to='django_reprepro.Component')),
                ('dist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_reprepro.Distribution')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_reprepro.Package')),
            ],
        ),
        migrations.RemoveField(
            model_name='sourcepackage',
            name='arch',
        ),
    ]