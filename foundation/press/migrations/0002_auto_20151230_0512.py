# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('press', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
        ),
    ]
