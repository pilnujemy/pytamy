# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings



class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0010_auto_20151126_1921'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('letters', '0007_letter_msg'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingLetter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_email', models.CharField(help_text='Field valid only for incoming messages', max_length=100, null=True, verbose_name='From e-mail')),
            ],
            options={
                'verbose_name': 'Incoming letter',
                'verbose_name_plural': 'Incoming letters',
            },
        ),
        migrations.CreateModel(
            name='OutgoingLetter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_send_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Outgoing letter',
                'verbose_name_plural': 'Outgoing letters',
            },
        ),
        migrations.AddField(
            model_name='outgoingletter',
            name='parent',
            field=models.OneToOneField(null=True, blank=True, to='letters.Letter'),
        ),
        migrations.AddField(
            model_name='outgoingletter',
            name='temp_author',
            field=models.ForeignKey(related_name='author_letter', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='outgoingletter',
            name='temp_email',
            field=models.ForeignKey(blank=True, to='offices.Email', null=True),
        ),
        migrations.AddField(
            model_name='outgoingletter',
            name='temp_sender',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='incomingletter',
            name='parent',
            field=models.OneToOneField(null=True, blank=True, to='letters.Letter'),
        ),
        migrations.AddField(
            model_name='incomingletter',
            name='temp_sender',
            field=models.ForeignKey(related_name='sender_office', blank=True, to='offices.Office', null=True),
        ),
    ]
