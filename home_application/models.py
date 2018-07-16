# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from django.db import models


class AlertSetting(models.Model):
    time_set = models.IntegerField(default=30)
    mailbox = models.CharField(max_length=200, null=True, default="")


class CerInfo(models.Model):
    issuer = models.TextField()
    effective_time = models.CharField(max_length=100)
    expired_time = models.CharField(max_length=100)
    subject = models.TextField()
    subject_altname = models.TextField()
    serial_number = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    # url:访问的IP或域名
    business = models.CharField(max_length=100)
    created_time = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def toDic(self):
        return_data = dict(
            [(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields] if attr != "created_by"])
        return return_data

