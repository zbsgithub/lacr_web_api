# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters.rest_framework as filters
from .models import StdChName, AliasChName


class StdChFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    alias_name = filters.CharFilter(lookup_expr="icontains", fileld_name='aliaschnames__name')

    class Meta:
        model = StdChName
        fields = ["name", "alias_name"]


class AliasChFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = AliasChName
        fields = ["name", ]
