# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('template', views.LogoTempView)
# router.register('operat_tem',views.LogotemplatBatchOperaView)
router.register('batch_opera',views.BatchOperatorLogoTempView)

urlpatterns = [
    re_path('^', include(router.urls))
]




