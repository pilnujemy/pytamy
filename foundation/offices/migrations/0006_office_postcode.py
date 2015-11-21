# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0005_auto_20151120_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='postcode',
            field=models.CharField(max_length=6, null=True, verbose_name='POst code'),
        ),
    ]
