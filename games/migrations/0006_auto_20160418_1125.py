# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-18 15:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_auto_20160417_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbet',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
