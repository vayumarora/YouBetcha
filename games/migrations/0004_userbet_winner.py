# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-18 01:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0003_auto_20160331_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbet',
            name='winner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
