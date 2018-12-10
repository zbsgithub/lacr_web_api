#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 13:53
# @Author  : zbs
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm

'''
序列化相关对象
'''
from rest_framework import serializers
from .models import CompanyDeviceStatistic



class CompanyDeviceStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDeviceStatistic
        fields = "__all__"

class MacOverViewListSerialize(serializers.ListSerializer):
    def get_default(self, validated_data):
        ret = []
        for item in validated_data:
            print("valid data: ", validated_data)
            my_id = item["id"]
            item_instance = CompanyDeviceStatistic.objects.get(pk=my_id)
            ret.append(item_instance)

        return ret