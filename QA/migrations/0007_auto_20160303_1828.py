# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-03 18:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0006_question_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category5', to='QA.Categories'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='category1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category1', to='QA.Categories'),
        ),
        migrations.AlterField(
            model_name='question',
            name='category2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category2', to='QA.Categories'),
        ),
        migrations.AlterField(
            model_name='question',
            name='category3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category3', to='QA.Categories'),
        ),
        migrations.AlterField(
            model_name='question',
            name='category4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category4', to='QA.Categories'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='upvote',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QA.Answer'),
        ),
        migrations.AlterField(
            model_name='upvote',
            name='upvoted_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]