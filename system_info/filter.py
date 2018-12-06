# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters.rest_framework as filters
from .models import StdChName, AliasChName


class StdChFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    abs_name = filters.CharFilter(field_name="name", lookup_expr="exact")

    class Meta:
        model = StdChName
        fields = ["name", "abs_name", ]


class AliasChFilters(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    abs_name = filters.CharFilter(field_name="name", lookup_expr="exact")

    class Meta:
        model = AliasChName
        fields = ["name", "abs_name", ]
