# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('subject', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', verbose_name='Slug', editable=False)),
                ('email', models.EmailField(max_length=250)),
                ('incoming', models.BooleanField(default=False, help_text='Is it a incoming message? Otherwise, it is outgoing.', verbose_name='Incoming')),
                ('eml', models.FileField(upload_to=b'eml_msg/%Y/%m/%d/')),
                ('letter', models.ForeignKey(verbose_name=b'Letter', to='letters.Letter')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
