# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_mailbox', '0004_bytestring_to_unicode'),
        ('letters', '0006_auto_20151127_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='msg',
            field=models.ForeignKey(blank=True, to='django_mailbox.Message', help_text='Message registered by django_mailbox', null=True),
        ),
    ]
