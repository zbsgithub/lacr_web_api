"""lacr_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, include
import logotemplat.urls
import system_info.urls
import statistics_info.urls
import user.urls

from lacr_api.settings import MEDIA_ROOT, MEDIA_URL
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^logotemplat/', include(logotemplat.urls)),
    re_path('^systeminfo/', include(system_info.urls)),
    re_path('^datastatistic/', include(statistics_info.urls)),#统计相关接口

    re_path('^user_login/', include(user.urls)),#统计相关接口

    re_path('^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    re_path('^docs/', include_docs_urls(title='LACR API')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
