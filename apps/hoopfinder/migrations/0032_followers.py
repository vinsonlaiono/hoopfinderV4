# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoopfinder', '0031_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('date_updated', models.DateTimeField(blank=True, null=True)),
                ('is_follow', models.BooleanField(default=True, verbose_name=b'Followed')),
                ('followers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='hoopfinder.User')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='hoopfinder.User')),
            ],
            options={
                'verbose_name': 'Followers',
                'verbose_name_plural': 'Followers',
            },
        ),
    ]
