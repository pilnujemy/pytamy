# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=2, editable=False, populate_from=b'name', unique=True),
            preserve_default=False,
        ),
    ]
