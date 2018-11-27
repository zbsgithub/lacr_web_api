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


from django.core.exceptions import ObjectDoesNotExist


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class ChannelNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChannelName
        fields = "__all__"


class ChNameCreateSerializer(serializers.ModelSerializer):
    channelnames = ChannelNameSerializer(help_text="频道名称")

    class Meta:
        model = ChannelType
        fields = ("name", "alias", "channelnames")

    def is_valid(self, raise_exception=False):
        return True

    def create(self, validated_data):
        channels_valid_data = validated_data.pop("channelnames")

        try:
            type_obj = ChannelType.objects.get(name=validated_data["name"])
        except ObjectDoesNotExist:
            type_obj = ChannelType.objects.create(**validated_data)

        channel_id = channels_valid_data["chid"]
        if not channel_id:
            channel_id = uuid.uuid4()
            cur_time = datetime.datetime.now()
            channels_valid_data["chid"] = "%s-%2d%s" % (channel_id, cur_time.second, cur_time.microsecond)

        try:
            ChannelName.objects.get(name=channels_valid_data["name"])
        except ObjectDoesNotExist:
            ChannelName.objects.create(**channels_valid_data)

        return type_obj
