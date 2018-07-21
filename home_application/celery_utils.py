# -*- coding: utf-8 -*-
from common.log import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from home_application.models import CerInfo, AlertSetting
import datetime


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
    _from = "160146764@qq.com"
    content_type = "HTML"
    conn_type = "NORMAL"
    is_anonymous = False
    pwd = "hjxvdzkrqkfbbihi"
    host = "smtp.qq.com"
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
    except Exception as e:
        return False, str(e)


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


def get_warn_cert_list():
    alert_setting = AlertSetting.objects.first()
    mail_to = alert_setting.mailbox.split(";")
    time_set = alert_setting.time_set
    date_now = datetime.datetime.now()
    date_delay = datetime.timedelta(days=time_set)
    date_warn = str(date_now + date_delay).split(".")[0]
    warn_cer_list = CerInfo.objects.filter(is_deleted=False, expired_time__range=(get_time_now_str(), date_warn))
    return warn_cer_list, mail_to


def get_time_now_str():
    date_now = datetime.datetime.now()
    date_now_str = str(date_now).split(".")[0]
    return date_now_str