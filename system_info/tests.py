from django.test import TestCase

# Create your tests here.
import requests


def inner_category_en():
    data = {
        "name": "卫视",
        "alias": "卫视, 卫视频道",
        "channelnames": {
            "chid": "",
            "name": "青海卫视",
            "alias": "青海卫视, 青海卫视频道"
        }
    }

    type_resp

    req_url = "http://47.93.181.56:5081/systeminfo/chtype/"

    resp = requests.post(req_url, json=data)
    print(resp.text)
    print(resp.status_code)
