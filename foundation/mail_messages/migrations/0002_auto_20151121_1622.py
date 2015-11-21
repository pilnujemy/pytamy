# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mail_messages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'subject', verbose_name='Slug', editable=False),
        ),
    ]
