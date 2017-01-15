# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-14 17:06
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentsFlowApp', '0002_auto_20170112_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='version',
            field=models.DecimalField(decimal_places=4, default=Decimal('0.0000'), max_digits=20),
        ),
    ]
