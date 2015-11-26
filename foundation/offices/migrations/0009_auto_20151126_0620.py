# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0008_auto_20151121_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='postcode',
            field=models.CharField(max_length=6, null=True, verbose_name='Post code', blank=True),
        ),
    ]
