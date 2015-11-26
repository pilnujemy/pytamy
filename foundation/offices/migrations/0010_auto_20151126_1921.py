# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0009_auto_20151126_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='regon',
            field=models.CharField(max_length=10, blank=True, help_text='Compatible with National Official Register of National Economy Entities', null=True, verbose_name='REGON', db_index=True),
        ),
    ]
