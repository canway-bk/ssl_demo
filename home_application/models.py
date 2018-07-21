# -*- coding: utf-8 -*-
from django.db import models


# 告警设置
class AlertSetting(models.Model):
    time_set = models.IntegerField(default=30)
    mailbox = models.CharField(max_length=200, null=True, default="")


# 告警历史
class AlertHistory(models.Model):
    app_name = models.CharField(max_length=100)
    when_expired = models.CharField(max_length=100)
    when_alert = models.CharField(max_length=100)
    mail_to = models.CharField(max_length=100)


# 证书数据
class CerInfo(models.Model):
    issuer = models.TextField()
    effective_time = models.CharField(max_length=100)
    expired_time = models.CharField(max_length=100)
    subject = models.TextField()
    subject_altname = models.TextField()
    serial_number = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    business = models.CharField(max_length=100)
    created_time = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def toDic(self):
        return_data = dict(
            [(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields] if attr != "created_by"])
        return return_data

