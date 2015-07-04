# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'correspondence_attachment', verbose_name=b'File')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('street', models.CharField(max_length=250, null=True, verbose_name='City', blank=True)),
                ('city', models.CharField(max_length=250, null=True, verbose_name='City', blank=True)),
                ('postcode', models.CharField(max_length=5, verbose_name='Post-code')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified on', null=True)),
                ('created_by', models.ForeignKey(related_name='contact_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='contact_modified', verbose_name='Modified by', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('outgoing', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, verbose_name='Modified on', null=True)),
                ('contact', models.ForeignKey(verbose_name='Contact', to='correspondence.Contact')),
                ('created_by', models.ForeignKey(related_name='letter_created', verbose_name='Created by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='letter_modified', verbose_name='Modified by', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='letter',
            field=models.ForeignKey(verbose_name='Letter', to='correspondence.Letter'),
        ),
    ]
