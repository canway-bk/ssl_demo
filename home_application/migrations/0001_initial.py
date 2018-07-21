# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlertHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(max_length=100)),
                ('when_expired', models.CharField(max_length=100)),
                ('when_alert', models.CharField(max_length=100)),
                ('mail_to', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AlertSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_set', models.IntegerField(default=30)),
                ('mailbox', models.CharField(default=b'', max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CerInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issuer', models.TextField()),
                ('effective_time', models.CharField(max_length=100)),
                ('expired_time', models.CharField(max_length=100)),
                ('subject', models.TextField()),
                ('subject_altname', models.TextField()),
                ('serial_number', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('business', models.CharField(max_length=100)),
                ('created_time', models.CharField(max_length=100)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
