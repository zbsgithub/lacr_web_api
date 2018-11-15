# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import requests
from urllib import urlencode


logger = logging.getLogger(__name__)
HTTP_URL = "http://api.map.baidu.com/location/ip"
HTTPS_URL = "https://api.map.baidu.com/location/ip"
IP_API_AK = "rQaQCwa69NU9HZX7aQ2IehWEBhLXpGmn"


def ip_location(ip):
    query = {
        "ip": ip,
        "ak": IP_API_AK,
    }
    resp = requests.get(HTTP_URL + "?" + urlencode(query))

    try:
        assert resp.status_code == 200
        s = resp.json()
        return s
    except:
        return None
