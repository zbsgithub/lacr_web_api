# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters.rest_framework as filters
from .models import LogoTemplate


class LogoTempFilters(filters.FilterSet):
    machine = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = LogoTemplate
        fields = ["machine", ]




