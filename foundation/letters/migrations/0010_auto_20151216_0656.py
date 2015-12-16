# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0009_auto_20151216_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomingletter',
            name='id',
        ),
        migrations.RemoveField(
            model_name='outgoingletter',
            name='id',
        ),
        migrations.AlterField(
            model_name='incomingletter',
            name='letter_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='letters.Letter'),
        ),
        migrations.AlterField(
            model_name='outgoingletter',
            name='letter_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='letters.Letter'),
        ),
    ]
