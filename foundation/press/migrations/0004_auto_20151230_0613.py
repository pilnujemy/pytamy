# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('press', '0003_auto_20151230_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=ckeditor.fields.RichTextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=ckeditor.fields.RichTextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
