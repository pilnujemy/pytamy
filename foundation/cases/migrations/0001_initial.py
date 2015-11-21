# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.utils.timezone
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0008_auto_20151121_0353'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', verbose_name='Slug', editable=False)),
                ('receiving_email', models.CharField(help_text='Address used to receiving emails.', max_length=150, verbose_name='Receiving email')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('office', models.ForeignKey(to='offices.Office')),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'Case',
                'verbose_name_plural': 'Cases',
            },
        ),
    ]
