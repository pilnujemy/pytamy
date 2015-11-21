# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0004_auto_20151021_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='officestatelog',
            name='on',
        ),
        migrations.RemoveField(
            model_name='officestatelog',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='email',
            options={'verbose_name': 'E-mail address', 'verbose_name_plural': 'E-mail addresses'},
        ),
        migrations.AlterModelOptions(
            name='office',
            options={'verbose_name': 'Office', 'verbose_name_plural': 'Offices'},
        ),
        migrations.RemoveField(
            model_name='office',
            name='state',
        ),
        migrations.RemoveField(
            model_name='office',
            name='verified',
        ),
        migrations.AddField(
            model_name='office',
            name='krs',
            field=models.CharField(help_text='Compatible with Polish National Court Register', max_length=9, null=True, verbose_name='Registration number', db_index=True),
        ),
        migrations.AddField(
            model_name='office',
            name='regon',
            field=models.CharField(null=True, max_length=10, help_text='Compatible with National Official Register of National Economy Entities', unique=True, verbose_name='REGON', db_index=True),
        ),
        migrations.AddField(
            model_name='office',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='Verified'),
        ),
        migrations.AlterField(
            model_name='office',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Name'),
        ),
        migrations.DeleteModel(
            name='OfficeStateLog',
        ),
    ]
