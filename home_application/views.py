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

from common.mymako import render_mako_context, render_json
from home_application.celery_tasks import execute_task


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


from home_application.utils import *

# 查询证书列表
def search_cer(request):
    cer_list = CerInfo.objects.filter(is_deleted=False).order_by("-created_time")
    return_data = []
    for i, cert in enumerate(cer_list):
        return_data.append(convert_cert_to_dict(cert, i))
    data = {"catalogues": catalogues, "items": return_data}
    return render_json(data)


# 新增证书
def add_cer(request):
    cer_obj = eval(request.body)
    res, msg = add_cer_main(cer_obj)
    return render_json({"result": res, "message": msg})


# 删除证书
def delete_cer(request):
    cer_id = request.GET.get("cer_id")
    CerInfo.objects.filter(id=cer_id).delete()
    return render_json({"result": True})


# 获取各CA证书数量统计
def get_ca_count(request):
    return_data = get_ca_count_main()
    return render_json(return_data)


# 获取各状态证书数量统计
def get_status_count(request):
    return_data = get_status_count_main()
    return render_json(return_data)


# 获取告警配置
def get_alert_setting(request):
    alert_setting = get_alert_setting_main()
    return render_json({"result": True, "data": {"time_set": alert_setting.time_set, "mailbox": alert_setting.mailbox}})


# 更新告警配置
def update_alert_setting(request):
    data = eval(request.body)
    res, msg = update_settings_main(data)
    return render_json({"result": res, "message": msg})


# 获取告警历史
def get_alert_history(request):
    data = get_alert_history_main()
    return render_json(data)


# 立即触发监控任务
def run_task(request):
    res, message = execute_task()
    return render_json({"result": res, "message": message})


