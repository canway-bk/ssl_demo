# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminWarnSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
        migrations.CreateModel(
            name='UserMsg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('time_set', models.IntegerField(default=30)),
                ('mailbox', models.CharField(default=b'', max_length=100, null=True)),
                ('is_all', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='cerinfo',
            name='created_by',
            field=models.ForeignKey(to='home_application.UserMsg'),
        ),
        migrations.AddField(
            model_name='adminwarnset',
            name='cer_info',
            field=models.ForeignKey(to='home_application.CerInfo'),
        ),
        migrations.AddField(
            model_name='adminwarnset',
            name='user_msg',
            field=models.ForeignKey(to='home_application.UserMsg'),
        ),
    ]
