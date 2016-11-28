# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20161123_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('date',)},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='events',
        ),
        migrations.AddField(
            model_name='event',
            name='team',
            field=models.ManyToManyField(to='app.Team'),
        ),
        migrations.AlterField(
            model_name='event',
            name='visibility',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], max_length=7),
        ),
    ]
