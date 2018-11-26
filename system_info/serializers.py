#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 15:33
# @Author  : zbs
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from .models import Company,Brand, ChannelType, ChannelName
from rest_framework import serializers
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

    def create(self, validated_data):
        print("not type exist-------------", validated_data)
        channels_valid_data = validated_data.pop("channelnames")

        try:
            type_obj = ChannelType.objects.get(name=validated_data["name"])
        except ObjectDoesNotExist:
            print("not type exist-------------")
            type_obj = ChannelType.objects.create(**validated_data)

        try:
            ChannelName.objects.get(name=channels_valid_data["name"])
        except ObjectDoesNotExist:
            print("not name exist-------------")
            ChannelName.objects.create(**validated_data)

        return type_obj
