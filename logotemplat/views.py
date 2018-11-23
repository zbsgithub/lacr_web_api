from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from .serializers import LogoTemplateSerializer, MachineListSerializer,LogoTemplateBulkSerializer
from .models import LogoTemplate
from .filter import LogoTempFilters
from django.db.models import Count
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
import rest_framework.status as status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import *
from django.shortcuts import get_object_or_404

import logging

class LogoTempView(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    delete:

    > 删除

    - `设置校验位: ` http://47.93.181.56:5081/logotemplat/template/{模型id}


    patch:

    > 设置

    - `设置校验位: ` http://47.93.181.56:5081/logotemplat/template/{模型id}

    - `请求数据: `

            {
                "checked": true,
            }

    list:

    > 台标特征列表

    - `所有设备列表: ` http://47.93.181.56:5081/logotemplat/template/?machine_list=1

            {
                "count": 1548,
                "next": "下一页地址",
                "previous": null,
                "results": [
                    {

                        "machine": "机器名1"
                        # 已有特征数
                        "model_num": 1
                    },
                    {
                        "machine": "机器名2"
                        "model_num": 1
                    },
                    ...
                ]
            }


    - `指定设备的特征: ` http://47.93.181.56:5081/logotemplat/template/?machine=设备名字

            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "temp": "特征图片地址",
                        "mask": "特征掩码图片地址",
                        "best": "抽样图片地址",

                        # 台标id
                        "cid": 46002,

                         # 台标唯一标识
                        "chuid": "a41afa10-8584-4910-975d-575f3c87f9f0",

                        # 勾正台标id
                        "gzcid": "b012e218-ca65-4d66-8eaf-8e13fc90e30a",

                        # 勾正台标名字
                        "gzchname": "Q0NUVjPnu7zoibpIRA==",

                        # 勾正台标类型
                        "gzchtype": "Q0NUVg==",

                        # 品牌名
                        "company": "skyworth",

                        # 屏幕类型
                        "ledmodel": "8H71",

                        # 电视类型
                        "tvmodel": "E6000",

                        # 勾正did
                        "did": "60427f401368",

                        # 勾正gzid
                        "gzid": "7d39a681-10c2-24f9-f74b-8eb6166d107c",

                        # 区域
                        "region": "900000",

                        # 机器
                        "machine": "7d39a681-10c2-24f9-f74b-8eb6166d107c_60427f401368",

                        # 坐标
                        "x": 38,
                        "y": 39,
                        "w": 100,
                        "h": 57,

                        # 匹配值
                        "match": 0,

                        # 奖励
                        "award": 19,

                        # 像素
                        "pixes": 57,

                        # 人工校验过
                        "checked": false,
                        "created_at": "2018-11-16 10:02:30",
                        "updated_at": "2018-11-16 10:02:30"
                    },
                    ...
                ]
            }

    - `状态码: `: 200


    """
    serializer_class = LogoTemplateSerializer
    queryset = LogoTemplate.objects.all()
    filter_class = LogoTempFilters

    @staticmethod
    def get_machine_list(queryset):
        return queryset.values_list("machine").annotate(model_num=Count("machine")).values("machine", "model_num")

    def get_queryset(self):
        machine_list = int(self.request.query_params.get("machine_list", 0))
        if machine_list == 1:
            return self.get_machine_list(self.queryset)
        else:
            return self.queryset

    def get_serializer_class(self):
        machine_list = 0
        try:
            machine_list = int(self.request.query_params.get("machine_list", 0))
        except:
            pass

        if machine_list == 1:
            return MachineListSerializer
        else:
            return self.serializer_class

# class LogotemplatBatchOperaView(viewsets.ModelViewSet):
#
#     """
#     batch_delete:
#
#     > 批量删除
#
#     - `批量删除: ` http://47.93.181.56:5081/logotemplat/template/batch_delete
#
#     """
#
#     queryset = LogoTemplate.objects.all()
#     serializer_class = LogoTemplateBulkSerializer
#     filter_class = LogoTempFilters
#
#     def batch_list(self):
#         return self.queryset
#
#     def batch_delete(self):
#         print('------------------------')
#         array = self.request.POST.getlist('ids')  # django接收数组
#         idstring = ','.join(array)
#         LogoTemplate.objects.extra(where=['id IN (' + idstring + ')']).delete()
#         return self.serializer_class
#
#     def perform_destroy(self, instance):
#         pass

"""
批量操作
"""
class BatchOperatorLogoTempView(viewsets.ModelViewSet):
    # permission_classes = (AllowAny)
    queryset = LogoTemplate.objects.all()
    serializer_class = LogoTemplateBulkSerializer
    filter_class = LogoTempFilters


    def get_serializer(self, *args, **kwargs):
        print("kwargs----------->", kwargs)
        try:
            data = kwargs.get('data', None)
            assert data
            if isinstance(data, list):
                kwargs["many"] = True
        except AssertionError:
            pass

        return super(BatchOperatorLogoTempView, self).get_serializer(*args, **kwargs)

    def multi_destroy(self):
        queryset = self.queryset

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        lookup_url_value = self.kwargs[lookup_url_kwarg]
        lookup_url_value_list = lookup_url_value.split(',')
        print("list: ", lookup_url_value_list)

        for lookup_url_value in lookup_url_value_list:
            filter_kwargs = {self.lookup_field: lookup_url_value}
            obj = get_object_or_404(queryset, **filter_kwargs)
            self.perform_destroy(obj)

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        print("批量删除：-------------------")
        return self.multi_destroy()

    # def partial_update(self, request, *args, **kwargs):
    #
    #     print("批量修改：")
    #     queryset = self.queryset
    #
    #     # Perform the lookup filtering.
    #     lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
    #
    #     assert lookup_url_kwarg in self.kwargs, (
    #             'Expected view %s to be called with a URL keyword argument '
    #             'named "%s". Fix your URL conf, or set the `.lookup_field` '
    #             'attribute on the view correctly.' %
    #             (self.__class__.__name__, lookup_url_kwarg)
    #     )
    #
    #     lookup_url_value = self.kwargs[lookup_url_kwarg]
    #     lookup_url_value_list = lookup_url_value.split(',')
    #     print("list: ", lookup_url_value_list)
    #     for lookup_url_value in lookup_url_value_list:
    #         filter_kwargs = {self.lookup_field: lookup_url_value}
    #         obj = get_object_or_404(queryset, **filter_kwargs)
    #         self.perform_update(obj)
    #
    #     return Response(status=status.HTTP_200_OK)
