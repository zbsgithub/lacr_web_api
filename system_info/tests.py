from django.test import TestCase

# Create your tests here.
import requests
import json
import base64


def inner_category_en():
    data_type = {
        "name": "卫视",
        "alias": "卫视, 卫视频道",
    }

    s = open("/Users/dkos/Downloads/130_4482490c-dfec-11e8-8fb9-00163e002cf2.jpg", "rb")
    base64_content = base64.b64encode(s.read())
    print(base64_content)

    data_name = {
        "classify": "",
        "chid": "NONE",
        "name": "青海卫视",
        "alias": "青海卫视, 青海卫视频道",
        "image": "data:image/jpg;base64," + str(base64_content, encoding="utf-8"),
    }

    req_url = "http://47.93.181.56:5081/systeminfo/chtype/"
    resp = requests.get("%s?name=%s" % (req_url, data_type["name"]))
    resp_js = resp.json()
    if resp_js["count"] > 1:
        print("more than one record")
        return
    elif resp_js["count"] == 1:
        print("has recored", resp_js)
        type_id = resp_js["results"][0]["id"]
    else:
        resp = requests.post(req_url, json=data_type)
        resp_js = resp.json()
        type_id = resp_js["id"]
        print("create new record")

    req_name_url = "http://47.93.181.56:5081/systeminfo/chname/"
    data_name["classify"] = type_id
    resp = requests.get("%s?name=%s" % (req_name_url, data_type["name"]))
    resp_js = resp.json()
    if resp_js["count"] > 1:
        print("more than one record")
        return
    elif resp_js["count"] == 1:
        print("has recored")
        print(resp_js)
    else:
        resp = requests.post(req_name_url, json=data_name)
        resp_js = resp.json()
        print("create new record", resp_js)
