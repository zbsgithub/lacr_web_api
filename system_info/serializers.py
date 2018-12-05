#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 15:33
# @Author  : zbs
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from .models import Company,Brand, StdChName, AliasChName
from rest_framework import serializers
from utils.serializers import Base64ImageField


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class AliasChSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, help_text="id")

    class Meta:
        model = AliasChName
        fields = "__all__"


class StdChSerializer(serializers.ModelSerializer):
    image = Base64ImageField(help_text="台标图片", required=False)
    alias = AliasChSerializer(source="get_alias", many=True, read_only=True, help_text="别名列表")

    class Meta:
        model = StdChName
        fields = ("ch_id", "name", "image", "created_at", "updated_at", "alias")


