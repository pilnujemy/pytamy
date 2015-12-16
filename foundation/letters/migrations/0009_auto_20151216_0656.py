# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def split_models(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    L = apps.get_model("letters", "Letter")
    OL = apps.get_model("letters", "OutgoingLetter")
    IL = apps.get_model("letters", "IncomingLetter")

    for letter in L.objects.filter(incoming=True).all():
        IL.objects.create(parent=letter,
                          temp_email=letter.email,
                          temp_sender=letter.sender_office)
    for letter in L.objects.filter(incoming=False).all():
        OL.objects.create(parent=letter,
                          temp_send_at=letter.send_at,
                          temp_sender=letter.sender_user,
                          temp_author=letter.author,
                          temp_email=letter.email)


class Migration(migrations.Migration):
    dependencies = [
        ('letters', '0008_auto_20151216_0647'),
    ]

    operations = [
        migrations.RunPython(split_models),
    ]
