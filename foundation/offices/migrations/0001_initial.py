# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields
import django_states.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teryt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Address')),
                ('default', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=150, verbose_name='Nazwa')),
                ('state', django_states.fields.StateField(default=b'created', max_length=100)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('jst', models.ForeignKey(to='teryt.JST')),
                ('parent', models.ManyToManyField(related_name='parent_rel_+', to='offices.Office')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfficeStateLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', django_states.fields.StateField(default=b'transition_initiated', max_length=100, verbose_name='state id')),
                ('from_state', models.CharField(max_length=100, choices=[(b'removed', 'Removed'), (b'accepted', 'Accepted'), (b'created', 'Office created')])),
                ('to_state', models.CharField(max_length=100, choices=[(b'removed', 'Removed'), (b'accepted', 'Accepted'), (b'created', 'Office created')])),
                ('serialized_kwargs', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='transition started at', db_index=True)),
                ('on', models.ForeignKey(related_name='state_history', to='offices.Office')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'office transition',
            },
        ),
    ]
