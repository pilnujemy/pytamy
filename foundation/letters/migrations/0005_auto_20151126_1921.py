# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0004_auto_20151126_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'subject', unique=True, verbose_name='Slug'),
        ),
    ]
