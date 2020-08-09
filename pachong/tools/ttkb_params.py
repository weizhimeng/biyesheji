# -*- coding: utf-8 -*-
from tools.myrequests import _requests as requests
import json
import uuid
import hashlib
import ipdb

headers = {
             'qn-rid': 'C02E564A-335A-4EA9-A910-FEB279C81972',
             'Accept': '*/*',
             'qqnetwork': 'wifi',
             'qn-sig': 'F588D59276E1972F68DBCC18AF308AAD',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
             'Accept-Encoding': 'gzip, deflate',
             'Cookie': 'logintype=2',
             'Referer': 'http',
             'Content-Type': 'text/plain',
             'appver': '10.2.1_qnreading_4.8.90',
             'apptypeExt': 'qnreading',
             'ssid': 'alimama',
             'appversion': '4.8.90',
             'devid': 'B4BBBE66-1BC0-469E-BE27-D8F83848DDDD',
             'currentTab': 'kuaibao'
}


def params_gen():
    """Generate qn-rid, qn-sig, devid.
    :note: qn-rid = devid
    :return: A tuple of (qn_rid, qn_sig)
    """
    UUID = uuid.uuid4()
    qn_rid = UUID.urn.replace('urn:uuid:', '')
    base = 'appver=10.2.1_qnreading_4.8.90&cgi=getSubNewsChlidInterest&devid={0}&qn-rid={0}&secret=qn123456'.format(UUID)
    base = base.encode('utf-8')
    qn_sig = hashlib.md5(base).hexdigest().upper()
    return (qn_rid, qn_sig)


def headers_gen():
    """Generate request headers.

    :return: Request headers.
    """
    qn_rid, qn_sig = params_gen()
    headers['qn-rid'] = qn_rid
    headers['devid'] = qn_rid
    headers['qn-sig'] = qn_sig
    return headers


def comment_headers_gen():
    headers = {
    'accept-encoding': 'gzip,deflate',
    'referer': 'http://cnews.qq.com/cnews/android/',
    'user-agent': '%E5%A4%A9%E5%A4%A9%E5%BF%AB%E6%8A%A55000(android)',
    'cookie': 'lskey=; luin=; skey=; uin=; logintype=0;',
    'qn-sig': '9282746fb058ee47d693a030b491bdbd',
    'svqn': '1_4',
    'qn-rid': 'f4b92ad0-c060-46d3-bd81-9ff3391ce2ab',
    'snqn': 'KlXUUcg8/8RuLIx/KZbjildtpe0B5bm7Gq4fwJW82waImEKrdSfIZHjEGydG9phvjSMBAw4K1x7ZSn/eg3YGJpJUdQZjoHp3+m73P6soWDo08JZQXac5JwV/X4azIaFe0vl5Ntz1f8OHHYMgelaHrw==',
    'content-type': 'application/x-www-form-urlencoded',
    }
    qn_rid, qn_sig = params_gen()
    headers['qn-rid'] = qn_rid
    headers['devid'] = qn_rid
    headers['qn-sig'] = qn_sig
    return headers



