# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 08:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=b'correspondence_attachment', verbose_name=b'File')),
                ('protected', models.BooleanField(default=False, help_text='Unmark if safe for the rights of third parties', verbose_name='Content protected')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('street', models.CharField(blank=True, max_length=250, null=True, verbose_name='Street')),
                ('city', models.CharField(blank=True, max_length=250, null=True, verbose_name='City')),
                ('postcode', models.CharField(max_length=6, verbose_name='Post-code')),
                ('comment', models.TextField(verbose_name='Comment')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified on')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outgoing', models.BooleanField(default=True, verbose_name='Outgoing')),
                ('transfer_on', models.DateField(default=datetime.date.today, help_text='Receive date for incoming, send date for outgoing', verbose_name='Transfer on')),
                ('description', models.CharField(max_length=250, verbose_name='Description')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified on')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='correspondence.Contact', verbose_name='Contact')),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
            },
        ),
    ]
