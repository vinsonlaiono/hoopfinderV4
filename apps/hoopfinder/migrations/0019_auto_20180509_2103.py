# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-10 04:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoopfinder', '0018_auto_20180509_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='friended_by',
        ),
        migrations.AddField(
            model_name='friend',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoopfinder.User'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='hoopfinder.User'),
        ),
    ]
