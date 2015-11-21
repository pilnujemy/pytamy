# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0003_auto_20151019_0358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='office',
            options={'verbose_name': 'Office', 'verbose_name_plural': 'Offices', 'permissions': (('can_verify', 'Can verify offices'), ('can_destroy', 'Can destroy offices'))},
        ),
    ]
