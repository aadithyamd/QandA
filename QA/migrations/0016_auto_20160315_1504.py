# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-15 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0015_auto_20160314_1239'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['follow', '-timestamp']},
        ),
    ]
