# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from home_application.models import CerInfo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from common.log import logger


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def get_smtp_client(conn_type, is_anonymous, _from, pwd, host, port):
    if conn_type == 'NORMAL':
        s = smtplib.SMTP(host, port)
    elif conn_type == 'SSL':
        s = smtplib.SMTP_SSL(host, port)
    elif conn_type == 'TLS':
        s = smtplib.SMTP(host, port)
        s.ehlo()
        s.starttls()

    if not is_anonymous:
        s.login(_from, pwd)
    return s


def send_mail(subject, content, to):
    _from = "cwbk@canway.net"
    content_type = "HTML"
    conn_type = "NORMAL"
    is_anonymous = True
    pwd = "1qaz@WSX3edc"
    host = "mail.canway.net"
    port = "25"

    msg = MIMEMultipart()
    msg.attach(MIMEText(content.encode('utf-8'), content_type, 'utf-8'))
    msg["Subject"] = subject.encode('utf-8')
    msg["From"] = _from
    msg["To"] = ",".join(to)
    msg['Content-Type'] = 'Text/' + content_type

    try:
        s = get_smtp_client(conn_type, is_anonymous, _from, pwd, host, port)
        s.sendmail(_from, to, msg.as_string())
        s.quit()
        return True, 'success'
    except smtplib.SMTPException, e:
        error_msg = u'send email to {0} failed'.format(",".join(to))
        logger.exception(error_msg)
        return False, error_msg


def build_html_mail_content(cer_list):
    content = u"""<p>
        <span style="font-family:微软雅黑">亲爱的用户，您好！</span>
    </p>
    <p style="margin-left:28px">
        <span style="font-family:微软雅黑">
            您有证书即将过期，请及时处理，证书信息如下：
        </span>
    </p>
    <table cellspacing="0" cellpadding="0" style="font-family:微软雅黑">
        <tbody>
        <tr class="firstRow">
            <td style="font-size:14px;width:180px;border:1px solid windowtext;; background:#C5E0B3; padding: 0px 7px;">
                <span style="font-family:微软雅黑">业务系统</span>
            </td>
            <td style="font-size:14px;width:180px;background-color:#C5E0B3;padding:0 7px;border-width:1px;border-style:solid solid solid none;border-color:windowtext;">
                <span style="font-family:微软雅黑">访问地址</span>
            </td>
            <td style="font-size:14px;background-color:#C5E0B3;padding:0 7px;border-width:1px;border-style:solid solid solid none;border-color:windowtext;">
                <span style="font-family:微软雅黑">证书颁发机构</span>
            </td>
            <td style="font-size:14px;width:150px;background-color:#C5E0B3;padding:0 7px;border-width:1px;border-style:solid solid solid none;border-color:windowtext;">
                <span style="font-family:微软雅黑">过期时间</span>
            </td>
        </tr>
        {0}
        </tbody>
    </table>
    """
    table_tr = u"""<tr>
            <td style="font-size:14px;padding:0 7px;border-width:1px;border-style:none solid solid solid;border-color:windowtext;">
            {0}</td>
            <td  style="font-size:14px;padding:0 7px;border-style:none solid solid none;border-right-width:1px;border-bottom-width:1px;border-right-color:windowtext;border-bottom-color:windowtext;">
            {1}</td>
            <td style="font-size:14px;padding:0 7px;border-style:none solid solid none;border-right-width:1px;border-bottom-width:1px;border-right-color:windowtext;border-bottom-color:windowtext;">
            {2}</td>
            <td  style="font-size:14px;padding:0 7px;border-style:none solid solid none;border-right-width:1px;border-bottom-width:1px;border-right-color:windowtext;border-bottom-color:windowtext;">
            {3}</td>
        </tr>"""
    table_content = ""
    for i in cer_list:
        table_content += table_tr.format(i.business, i.url, i.issuer, i.expired_time)
    return content.format(table_content)


def execute_task():
    date_now = datetime.datetime.now()
    date_now_str = str(date_now).split(".")[0]
    date_delay = datetime.timedelta(days=330)
    date_warn = str(date_now + date_delay).split(".")[0]
    warn_cer_list = CerInfo.objects.filter(is_deleted=False, expired_time__range=(date_now_str, date_warn))
    content = build_html_mail_content(warn_cer_list)
    send_mail(u"SSL证书过期提醒", content, "landon@canway.net")


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))
