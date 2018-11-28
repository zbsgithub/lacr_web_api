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

    class Meta:
        model = Company
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class ChNameSerializer(serializers.ModelSerializer):
    image = Base64ImageField(help_text="台标图片")
    type_name = serializers.CharField(source="classify.name", read_only=True, help_text="分类名称")

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
    id = serializers.IntegerField(read_only=True, help_text="id")
    channel_count = serializers.IntegerField(source="get_channel_count", read_only=True, help_text="频道个数")

    class Meta:
        model = ChannelType
        fields = ("id", "name", "alias", "channel_count", "created_at", "updated_at")
