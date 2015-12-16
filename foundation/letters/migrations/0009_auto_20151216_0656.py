# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0008_auto_20151216_0647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incomingletter',
            old_name='parent',
            new_name='letter_ptr',
        ),
        migrations.RenameField(
            model_name='outgoingletter',
            old_name='parent',
            new_name='letter_ptr',
        ),
    ]
