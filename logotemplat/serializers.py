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
    model_num = serializers.BooleanField(read_only=True, help_text="模型数目")

    class Meta:
        model = LogoTemplate
        fields = ("machine", "model_num")
