#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 11:55
# @Author  : zbs
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from __future__ import unicode_literals
from django.urls import include, re_path,path
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# router.register('info', views.StatisticsInfoView)

urlpatterns = [
    # path('mac_overview', views.StatisticsInfoView.as_view(),name='mac_overview'),
    # path('brand_trend', views.StatisticsInfoView.as_view(),name='brand_trend'),
    re_path('^mac_overview', views.MacOverView.as_view()),
    re_path('^brand_trend', views.BrandTrendView.as_view()),
    re_path('^login', views.LoginView.as_view()),
    re_path('^get_info', views.GetUserInfo.as_view()),
    # re_path('^', include(router.urls))
]