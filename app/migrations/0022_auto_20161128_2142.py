# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 21:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20161128_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='team',
            field=models.ManyToManyField(blank=True, null=True, to='app.Team'),
        ),
        migrations.AlterField(
            model_name='event',
            name='visibility',
            field=models.CharField(choices=[('Private', 'Private'), ('Public', 'Public')], max_length=7),
        ),
    ]
