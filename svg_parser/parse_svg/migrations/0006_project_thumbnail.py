# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parse_svg', '0005_remove_project_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='thumbnail',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
