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

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^run_task$', 'run_task'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^search_crt/$', 'search_crt'),
    # 证书管理
    (r'^search_cer$', 'search_cer'),
    (r'^search_cer_for_admin$', 'search_cer_for_admin'),
    (r'^search_all_cer$', 'search_all_cer'),
    (r'^add_cer$', 'add_cer'),
    (r'^delete_cer$', 'delete_cer'),
    (r'^get_status_count$', 'get_status_count'),
    (r'^get_ca_count$', 'get_ca_count'),
    (r'^get_alert_setting$', 'get_alert_setting'),
    (r'^update_alert_setting$', 'update_alert_setting'),
    (r'^get_alert_history$', 'get_alert_history'),
)
