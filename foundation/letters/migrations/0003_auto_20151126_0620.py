# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('letters', '0002_auto_20151121_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetterAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='letter',
            name='name',
        ),
        migrations.AddField(
            model_name='letter',
            name='author',
            field=models.ForeignKey(related_name='author_letter', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='letter',
            name='eml',
            field=models.FileField(null=True, upload_to=b'eml_msg/%Y/%m/%d/', blank=True),
        ),
        migrations.AddField(
            model_name='letter',
            name='from_email',
            field=models.CharField(help_text='Field valid only for incoming messages', max_length=100, null=True, verbose_name='From e-mail'),
        ),
        migrations.AddField(
            model_name='letter',
            name='incoming',
            field=models.BooleanField(default=False, help_text='Is it a incoming message? Otherwise, it is outgoing.', verbose_name='Incoming'),
        ),
        migrations.AddField(
            model_name='letter',
            name='send_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='letter',
            name='subject',
            field=models.CharField(default=1, max_length=50, verbose_name='Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='letterauthor',
            name='letter',
            field=models.ForeignKey(verbose_name='Letter', to='letters.Letter'),
        ),
        migrations.AddField(
            model_name='letterauthor',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
