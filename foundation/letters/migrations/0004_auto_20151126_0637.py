# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0003_auto_20151126_0620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letterauthor',
            name='letter',
        ),
        migrations.RemoveField(
            model_name='letterauthor',
            name='user',
        ),
        migrations.DeleteModel(
            name='LetterAuthor',
        ),
    ]
