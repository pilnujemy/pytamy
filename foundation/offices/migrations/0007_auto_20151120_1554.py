# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('offices', '0006_office_postcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='extra',
            field=jsonfield.fields.JSONField(default=b'{}'),
        ),
        migrations.AddField(
            model_name='office',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='office',
            name='jst',
            field=models.ForeignKey(to='teryt.JST', blank=True),
        ),
        migrations.AlterField(
            model_name='office',
            name='krs',
            field=models.CharField(max_length=9, blank=True, help_text='Compatible with Polish National Court Register', null=True, verbose_name='Registration number', db_index=True),
        ),
        migrations.AlterField(
            model_name='office',
            name='parent',
            field=models.ManyToManyField(related_name='_parent_+', to='offices.Office', blank=True),
        ),
        migrations.AlterField(
            model_name='office',
            name='postcode',
            field=models.CharField(max_length=6, null=True, verbose_name='Post code'),
        ),
        migrations.AlterField(
            model_name='office',
            name='regon',
            field=models.CharField(null=True, max_length=10, blank=True, help_text='Compatible with National Official Register of National Economy Entities', unique=True, verbose_name='REGON', db_index=True),
        ),
    ]
