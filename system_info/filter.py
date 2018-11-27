# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters.rest_framework as filters
from .models import ChannelType, ChannelName


class ChannelTypeFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = ChannelType
        fields = ["name", ]


class ChannelNameFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = ChannelName
        fields = ["name", ]




