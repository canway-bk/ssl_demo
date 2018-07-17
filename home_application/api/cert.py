# -*- coding: utf-8 -*-
from common.mymako import render_json
from common.log import logger
from home_application.models import CerInfo, AlertSetting
from home_application.helper_view import *
import datetime


def search_cer(request):
    try:
        cer_list = CerInfo.objects.filter(
            is_deleted=False
        ).order_by("-created_time")

        return_data = []
        for i, cert in enumerate(cer_list):
            return_data.append(
                {
                    "id": cert.id,
                    "index": i,
                    "app_name": cert.business,
                    "username": cert.subject,
                    "url": cert.url,
                    "ef_date": cert.effective_time,
                    "ex_date": cert.expired_time
                }
            )

        data = {
            "catalogues": {
                "index": "序号",
                "app_name": "业务系统",
                "username": "使用者名称",
                "url": "访问地址",
                "ef_date": "生效时间",
                "ex_date": "过期时间"
            },
            "items": return_data
        }
        return render_json(data)
    except Exception, e:
        logger.exception(e.message)
        return render_json({"result": False, "data": [u"系统出错，请联系开发人员"]})


def add_cer(request):
    try:
        cer_obj = eval(request.body)
        username = request.user.username
        old_cer_len = CerInfo.objects.filter(url=cer_obj["url"]).count()
        if old_cer_len:
            return render_json({"result": False, "message": u"该证书已添加，无需重复添加"})
        date_now = str(datetime.datetime.now()).split(".")[0]
        cerinfo = get_cerinfo_by_url(cer_obj["url"])
        if not cerinfo["result"]:
            return render_json({"result": False, "message": cerinfo["message"]})

        cer_create = cerinfo["data"]
        CerInfo.objects.create(
            issuer=cer_create["issuer"],
            effective_time=cer_create["effective_time"],
            expired_time=cer_create["expired_time"],
            subject=cer_create["subject"],
            subject_altname=cer_create["subject_altname"],
            serial_number=cer_create["serial_number"],
            url=cer_obj["url"],
            business=cer_obj["app"],
            created_time=date_now
        )
        return render_json({"result": True})
    except Exception, e:
        logger.error(e)
        return render_json({"result": False, "message": u"系统出错，请联系开发人员"})


def delete_cer(request):
    try:
        cer_id = request.GET.get("cer_id")
        CerInfo.objects.filter(id=cer_id).delete()
        return render_json({"result": True})
    except Exception, e:
        logger.error(e)
        return render_json({"result": False, "message": u"系统出错，请联系开发人员"})


def get_ca_count(request):
    try:
        cer_names = CerInfo.objects.filter(is_deleted=False).values("issuer").distinct()

        categories = []
        data = []

        for i in cer_names:
            data.append(CerInfo.objects.filter(issuer=i["issuer"], is_deleted=False).count())
            categories.append(i["issuer"])

        return_data = {
            "code": 0,
            "result": True,
            "messge": "success",
            "data": {
                "series": [{
                    "name": "证书数量",
                    "data": data
                }],
                "categories": categories
            }
        }
        return render_json(return_data)

    except Exception, e:
        logger.error(e)
        return render_json({"result": False, "message": u"系统出错，请联系开发人员"})


def get_status_count(request):
    try:
        alert_setting = _get_alert_setting()
        time_set = alert_setting.time_set

        date_now = datetime.datetime.now()
        date_now_str = str(date_now).split(".")[0]
        date_delay = datetime.timedelta(days=time_set)
        date_warn = str(date_now + date_delay).split(".")[0]
        expired_len = CerInfo.objects.filter(is_deleted=False, expired_time__lte=date_now_str).count()
        warn_len = CerInfo.objects.filter(is_deleted=False, expired_time__range=(date_now_str, date_warn)).count()
        normal_len = CerInfo.objects.filter(is_deleted=False, expired_time__gt=date_warn).count()
        # return_data = [
        #     {"name": u"已过期", "y": expired_len, "color": "#f45b5b"},
        #     {"name": u"即将过期（30天）", "y": warn_len, "color": "#f7a35c"},
        #     {"name": u"正常状态", "y": normal_len, "color": "#90ed7d"}
        # ]
        return_data = {
            "code": 0,
            "result": True,
            "messge": "success",
            "data": {
                "title": "",
                "series": [{
                    "value": expired_len,
                    "name": "已过期"
                }, {
                    "value": warn_len,
                    "name": "即将过期（{0}天）".format(time_set),
                    "color": "#f7a35c"
                }, {
                    "value": normal_len,
                    "name": "正常状态"
                }]
            }
        }
        return render_json(return_data)
    except Exception, e:
        logger.error(e)
        return render_json({"result": False, "message": u"系统出错，请联系开发人员"})


def _get_alert_setting():
    alert_setting = AlertSetting.objects.all().first()
    if not alert_setting:
        alert_setting = AlertSetting()
        alert_setting.mailbox = ""
        alert_setting.time_set = 300
        alert_setting.save()
    return alert_setting


def get_alert_setting(request):
    alert_setting = _get_alert_setting()
    return render_json({"result": True, "data": {"time_set": alert_setting.time_set, "mailbox": alert_setting.mailbox}})


def update_alert_setting(request):
    data = eval(request.body)
    alert_setting = AlertSetting.objects.all().first()
    if not alert_setting:
        alert_setting = AlertSetting()

    alert_setting.mailbox = data["mailbox"]
    alert_setting.time_set = data["time_set"]
    alert_setting.save()
    return render_json({"result": True})


def get_alert_history(request):
    return_data = []
    return_data.append(
        {
            "index": 1,
            "app_name": "bk",
            "when_alert": "2017",
            "receiver": "landon@canway.net",
            "ex_date": "2018"
        }
    )

    data = {
        "catalogues": {
            "index": "序号",
            "app_name": "业务系统",
            "when_alert": "告警时间",
            "receiver": "告警接收人",
            "ex_date": "过期时间"
        },
        "items": return_data
    }
    return render_json(data)
