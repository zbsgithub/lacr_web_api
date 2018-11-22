# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from .models import LogoTemplate
from utils.serializers import Base64ImageField


class LogoTemplateSerializer(serializers.ModelSerializer):
    temp = Base64ImageField(help_text="台标特征")
    mask = Base64ImageField(help_text="台标掩码")
    best = Base64ImageField(help_text="抽样台标")

    class Meta:
        model = LogoTemplate
        fields = "__all__"


class MachineListSerializer(serializers.Serializer):
    model_num = serializers.IntegerField(read_only=True, help_text="模型数目")
    machine = serializers.CharField(help_text="设备名字")



class LogoTemplateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        print("valid data: ", validated_data)
        return super(LogoTemplateListSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(LogoTemplateSerializer, self).update(instance, validated_data)

class LogoTemplateBulkSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogoTemplate
        fields = "__all__"
        list_serializer_class = LogoTemplateListSerializer

    def create(self, validated_data):
        id = validated_data["id"]
        obj = LogoTemplate.objects.get(pk=id)
        super(LogoTemplateBulkSerializer, self).update(obj, validated_data);

        return obj
