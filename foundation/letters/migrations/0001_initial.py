# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django_bleach.models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0008_auto_20151121_0353'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', verbose_name='Slug', editable=False)),
                ('content', django_bleach.models.BleachField()),
                ('email', models.EmailField(max_length=254, verbose_name=b'offices.Email')),
                ('case', models.ForeignKey(to='cases.Case')),
                ('recipient', models.ForeignKey(blank=True, to='offices.Office', null=True)),
                ('sender_office', models.ForeignKey(related_name='sender_office', blank=True, to='offices.Office', null=True)),
                ('sender_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
            },
        ),
    ]
