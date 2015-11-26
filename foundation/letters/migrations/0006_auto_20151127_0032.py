# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0005_auto_20151126_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=b'letters/%Y/%m/%d', verbose_name='File')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
        migrations.AddField(
            model_name='letter',
            name='quote',
            field=django_bleach.models.BleachField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attachment',
            name='letter',
            field=models.ForeignKey(to='letters.Letter'),
        ),
    ]
