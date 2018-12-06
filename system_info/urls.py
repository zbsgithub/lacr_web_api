#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 15:26
# @Author  : zbs
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from __future__ import unicode_literals
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('company', views.CompanyView)
router.register('brand', views.BrandView)
router.register('std_ch', views.StdChViewSet)
router.register("alias_ch", views.AliasChViewSet)

urlpatterns = [
    re_path('^', include(router.urls))
]
