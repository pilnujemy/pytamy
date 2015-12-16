# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0010_auto_20151216_0656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incomingletter',
            old_name='temp_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='incomingletter',
            old_name='temp_sender',
            new_name='sender',
        ),
        migrations.RenameField(
            model_name='outgoingletter',
            old_name='temp_author',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='outgoingletter',
            old_name='temp_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='outgoingletter',
            old_name='temp_send_at',
            new_name='send_at',
        ),
        migrations.RenameField(
            model_name='outgoingletter',
            old_name='temp_sender',
            new_name='sender',
        ),
    ]
