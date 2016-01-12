# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0010_auto_20151126_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='jst',
            field=models.ForeignKey(verbose_name='Unit of administrative division', to='teryt.JST'),
        ),
        migrations.AlterField(
            model_name='office',
            name='parent',
            field=models.ManyToManyField(related_name='_office_parent_+', verbose_name='Offices Supervisory', to='offices.Office', blank=True),
        ),
        migrations.AlterField(
            model_name='office',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
