# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-15 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20160315_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrower',
            name='Ssn',
            field=models.CharField(max_length=200),
        ),
    ]
