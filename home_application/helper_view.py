# -*-coding:utf-8-*-
from socket import socket
from OpenSSL import SSL
import datetime
from common.log import logger


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
