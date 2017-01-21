# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-21 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentsFlowApp', '0004_document_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flux',
            name='users',
        ),
        migrations.RemoveField(
            model_name='template',
            name='flux',
        ),
        migrations.AddField(
            model_name='flux',
            name='name',
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='template',
            name='name',
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
    ]
