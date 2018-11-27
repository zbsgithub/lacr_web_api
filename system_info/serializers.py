#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 15:33
# @Author  : zbs
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from .models import Company,Brand, ChannelType, ChannelName
from rest_framework import serializers
import uuid
import datetime
from utils.serializers import Base64ImageField



class CompanySerializer(serializers.ModelSerializer):
    image = Base64ImageField(help_text="台标图片")

    class Meta:
        model = Company
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class ChNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChannelName
        fields = "__all__"

    def create(self, validated_data):
        channel_id = validated_data["chid"]
        if "NONE" == channel_id:
            channel_id = uuid.uuid4()
            cur_time = datetime.datetime.now()
            validated_data["chid"] = "%s-%2d%s" % (channel_id, cur_time.second, cur_time.microsecond)

        return super(ChNameSerializer, self).create(validated_data)


class ChTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChannelType
        fields = "__all__"
