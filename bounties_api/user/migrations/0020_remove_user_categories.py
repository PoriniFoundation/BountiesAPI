# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-04 20:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20180928_0349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='categories',
        ),
    ]