# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-12 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0008_question_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.CharField(choices=[('CS', 'Computer Science'), ('EC', 'Electronics & Communication'), ('EE', 'Electrical & Electronics'), ('EB', 'Electronics & Biomedical')], default='CS', max_length=2),
            preserve_default=False,
        ),
    ]
