#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 15:33
# @Author  : zbs
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from .models import Company,Brand, ChannelType, ChannelName
from rest_framework import serializers

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
    channels = ChannelNameSerializer(help_text="频道名称")

    class Meta:
        model = ChannelType
        fields = ("name", "alias", "channels")

    def create(self, validated_data):
        channels_valid_data = validated_data.pop("channels")

        type_obj = ChannelType.objects.create(**validated_data)
        channels_valid_data["classify"] = type_obj
        ChannelName.objects.create(**channels_valid_data)

        return type_obj
