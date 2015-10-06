# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correspondence', '0002_auto_20150704_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='protected',
            field=models.BooleanField(default=False, help_text='Unmark if safe for the rights of third parties', verbose_name='Content protected'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='description',
            field=models.CharField(max_length=250, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='outgoing',
            field=models.BooleanField(default=True, verbose_name='Outgoing'),
        ),
    ]
