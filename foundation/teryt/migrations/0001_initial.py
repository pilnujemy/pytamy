# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teryt_tree', '0006_auto_20151018_0204'),
    ]

    operations = [
        migrations.CreateModel(
            name='JST',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('teryt_tree.jednostkaadministracyjna',),
        ),
    ]
