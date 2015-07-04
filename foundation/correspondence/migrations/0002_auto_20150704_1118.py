# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('correspondence', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='description',
            field=models.CharField(default='default', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='letter',
            name='transfer_on',
            field=models.DateField(default=datetime.date.today, help_text='Receive date for incoming, send date for outgoing', verbose_name='Transfer on'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='postcode',
            field=models.CharField(max_length=6, verbose_name='Post-code'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='street',
            field=models.CharField(max_length=250, null=True, verbose_name='Street', blank=True),
        ),
    ]
