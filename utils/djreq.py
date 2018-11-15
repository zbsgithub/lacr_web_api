# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def remote_ip(req):
    if 'HTTP_X_FORWARDED_FOR' in req.META:
        ip = req.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = req.META.get('REMOTE_ADDR', None)

    return ip
