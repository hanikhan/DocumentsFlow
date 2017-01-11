# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-09 17:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assigment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentTypes', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=40)),
                ('templateValues', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Flux',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documents', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flux', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Flux')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline', models.DateField()),
                ('status', models.CharField(max_length=40)),
                ('assigment', models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Assigment')),
                ('process', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Process')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keys', models.CharField(max_length=256)),
                ('flux', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Flux')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_reader', models.BooleanField(default=True)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_contributor', models.BooleanField(default=False)),
                ('group', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='process',
            name='starter',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flux',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='task',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Task'),
        ),
        migrations.AddField(
            model_name='document',
            name='template',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Template'),
        ),
        migrations.AddField(
            model_name='assigment',
            name='flux',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='DocumentsFlowApp.Flux'),
        ),
        migrations.AddField(
            model_name='assigment',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
