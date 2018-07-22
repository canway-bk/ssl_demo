# -*- coding: utf-8 -*-
from celery.schedules import crontab
from celery.task import periodic_task

from home_application.celery_utils import *
from home_application.models import AlertHistory

def execute_task_main():
    # 获取即将过期的证书并发送邮件
    warn_cer_list, mail_to = get_warn_cert_list()
    if len(warn_cer_list) == 0 or len(mail_to) == 0:
        return True, ""

    content = build_html_mail_content(warn_cer_list)
    res, msg = send_mail(u"SSL证书过期提醒", content, mail_to)
    if not res:
        return res, msg

    # 记录告警历史
    for cer in warn_cer_list:
        AlertHistory.objects.create(app_name=cer.business,
                                    when_expired=cer.expired_time, when_alert=get_time_now_str(),
                                    mail_to=";".join(mail_to))
    return True, "success!"


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def execute_task():
    return execute_task_main()