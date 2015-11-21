# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letter',
            name='recipient',
        ),
        migrations.AlterField(
            model_name='letter',
            name='email',
            field=models.ForeignKey(blank=True, to='offices.Email', null=True),
        ),
        migrations.AlterField(
            model_name='letter',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', unique=True, verbose_name='Slug'),
        ),
    ]
