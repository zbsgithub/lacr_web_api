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

        ret = []
        for item in validated_data:
            print("valid data: ", validated_data)
            item_instance = LogoTemplate.objects.get(pk=validated_data.get["id"])
            ret.append(self.child.update(item_instance, item))

        return ret


class LogoTemplateBulkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=-1, help_text=u"分类id")

    class Meta:
        model = LogoTemplate
        fields = "__all__"
        list_serializer_class = LogoTemplateListSerializer

    def create(self, validated_data):
        id = validated_data["id"]
        obj = LogoTemplate.objects.get(pk=id)
        super(LogoTemplateBulkSerializer, self).update(obj, validated_data);

        return obj
