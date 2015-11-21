# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0007_auto_20151120_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='jst',
            field=models.ForeignKey(to='teryt.JST'),
        ),
    ]
