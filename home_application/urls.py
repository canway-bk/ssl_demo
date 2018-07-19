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

from django.conf.urls import patterns
from home_application.api import cert

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^search_cer$', cert.search_cer),
    (r'^add_cer$', cert.add_cer),
    (r'^delete_cer$', cert.delete_cer),
    (r'^get_status_count$', cert.get_status_count),
    (r'^get_ca_count$', cert.get_ca_count),
    (r'^get_alert_setting$', cert.get_alert_setting),
    (r'^update_alert_setting$', cert.update_alert_setting),
    (r'^get_alert_history$', cert.get_alert_history),
    (r'^run_task$', cert.run_task),
)
