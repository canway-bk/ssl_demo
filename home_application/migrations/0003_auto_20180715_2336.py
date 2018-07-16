# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_remove_cerinfo_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_set', models.IntegerField(default=30)),
                ('mailbox', models.CharField(default=b'', max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='adminwarnset',
            name='cer_info',
        ),
        migrations.RemoveField(
            model_name='adminwarnset',
            name='user_msg',
        ),
        migrations.DeleteModel(
            name='AdminWarnSet',
        ),
        migrations.DeleteModel(
            name='UserMsg',
        ),
    ]
