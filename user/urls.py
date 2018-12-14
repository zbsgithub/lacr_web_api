#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 21:09
# @Author  : zbs
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
    re_path(r'^login/',  views.UserLoginView.as_view()),
    re_path(r'^logout/', views.UserLogoutView.as_view()),
    re_path(r'^get_info/', views.UserGetInfo.as_view()),
]