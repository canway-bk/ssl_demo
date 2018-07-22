# -*- coding: utf-8 -*-
from home_application.models import CerInfo, AlertSetting, AlertHistory
from common.log import logger
import datetime
from socket import socket
from OpenSSL import SSL


catalogues = {"index": "序号", "app_name": "业务系统", "username": "使用者名称",
              "url": "访问地址",
              "ef_date": "生效时间",
              "ex_date": "过期时间"
              }


def convert_cert_to_dict(cert, i):
    return {"id": cert.id, "index": i + 1, "app_name": cert.business, "username": cert.subject, "url": cert.url,
            "ef_date": cert.effective_time,
            "ex_date": cert.expired_time}


def get_cerinfo_by_url(url):
    try:
        sslcontext = SSL.Context(SSL.TLSv1_METHOD)
        sslcontext.set_timeout(10)
        s = socket()
        s.connect((url, 443))
        c = SSL.Connection(sslcontext, s)
        c.set_connect_state()
        c.do_handshake()
        cer = c.get_peer_certificate()
        serial_number = cer.get_serial_number()
        issuer = X509NameToStr(cer.get_issuer())
        effective_time = UTCTimeToStr(cer.get_notBefore())
        expired_time = UTCTimeToStr(cer.get_notAfter())
        subject = X509NameToStr(cer.get_subject())
        i = 0
        subject_altname = ""
        while i < cer.get_extension_count():
            ex = cer.get_extension(i)
            if ex.get_short_name() == "subjectAltName":
                subject_altname = ex.__str__()
                break
            i += 1
        c.shutdown()
        s.close()
        return_data = {"issuer": issuer, "effective_time": effective_time, "expired_time": expired_time,
                       "subject": subject, "serial_number": str(serial_number), "subject_altname": subject_altname}
        return {"result": True, "data": return_data}
    except Exception as e:
        logger.exception(e)
        return {"result": False, "message": u"连接失败,请确认访问地址正确和网络是否连通, err: %s" % str(e)}


def X509NameToStr(x509name):
    str0 = ""
    for i in x509name.get_components():
        if i[0] == "CN":
            str0 = i[1]
            # str1 = i[0] + "=" + i[1]
            # str0 += (str1 + ", ")
    # return str0.strip(", ")
    return str0


def UTCTimeToStr(utc):
    return str(datetime.datetime.strptime(utc, "%Y%m%d%H%M%SZ") + datetime.timedelta(hours=8))


def get_alert_setting_main():
    alert_setting = AlertSetting.objects.all().first()
    if not alert_setting:
        alert_setting = AlertSetting()
        alert_setting.mailbox = ""
        alert_setting.time_set = 300
        alert_setting.save()
    return alert_setting


def add_cer_main(cer_obj):
    try:
        old_cer_len = CerInfo.objects.filter(url=cer_obj["url"]).count()
        if old_cer_len:
            return False, u"该证书已添加，无需重复添加"
        date_now = str(datetime.datetime.now()).split(".")[0]
        cer_info = get_cerinfo_by_url(cer_obj["url"])
        if not cer_info["result"]:
            return False, cer_info["message"]

        cer_create = cer_info["data"]
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
        return True, ""
    except Exception, e:
        logger.exception(e.message)
        return False, e.message


def get_ca_count_main():
    cer_names = CerInfo.objects.filter(is_deleted=False).values("issuer").distinct()
    categories = []
    data = []
    for i in cer_names:
        data.append(CerInfo.objects.filter(issuer=i["issuer"], is_deleted=False).count())
        categories.append(i["issuer"])
    return_data = {"code": 0, "result": True, "messge": "success",
                   "data": {
                       "series": [{
                           "name": "证书数量",
                           "data": data
                       }],
                       "categories": categories
                   }
                   }
    return return_data


def get_status_count_main():
    alert_setting = get_alert_setting_main()
    time_set = alert_setting.time_set
    date_now = datetime.datetime.now()
    date_now_str = str(date_now).split(".")[0]
    date_delay = datetime.timedelta(days=time_set)
    date_warn = str(date_now + date_delay).split(".")[0]
    expired_len = CerInfo.objects.filter(is_deleted=False, expired_time__lte=date_now_str).count()
    warn_len = CerInfo.objects.filter(is_deleted=False, expired_time__range=(date_now_str, date_warn)).count()
    normal_len = CerInfo.objects.filter(is_deleted=False, expired_time__gt=date_warn).count()
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
    return return_data


def get_alert_history_main():
    alert_history = AlertHistory.objects.all()
    return_data = []
    for i, h in enumerate(alert_history):
        return_data.append(
            {
                "index": i + 1,
                "app_name": h.app_name,
                "when_alert": h.when_alert,
                "receiver": h.mail_to,
                "ex_date": h.when_expired
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
    return data


def update_settings_main(data):
    alert_setting = AlertSetting.objects.all().first()
    if not alert_setting:
        alert_setting = AlertSetting()
    alert_setting.mailbox = data["mailbox"]
    alert_setting.time_set = data["time_set"]
    alert_setting.save()
    return True, ""