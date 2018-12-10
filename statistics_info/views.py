from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins,status
from .models import  CompanyDeviceStatistic
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MacOverViewListSerialize
from .serializers import CompanyDeviceStatisticSerializer
import logging

from django.core import serializers
import json
from rest_framework.views import APIView
# Create your views here.
import datetime
from .models import Company,SlaveDeviceStatistic,Slave

from django.http import HttpResponse
import time

'''
statistics about info
'''
class MacOverView(APIView):
    """
        get:

        > 设备统计信息

        # - 相关接口
    """

    def get(self, request, *args, **kwargs):

        result = {}

        # 先获得时间数组格式的日期
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))
        formate_time = yesterday.strftime("%Y-%m-%d")# %H:%M:%S
        print(formate_time)
        queryset = CompanyDeviceStatistic.objects.filter(created_at__gte=str(formate_time))
        print("集合大小：%d " % queryset.__len__())
        total_num = 0
        temp_array = []
        rgb_array = []
        rgb_array.append({'icon':'md-locate','color': '#19be6b'})
        rgb_array.append({'icon':'md-help-circle','color': '#ff9900'})
        rgb_array.append({'icon':'md-share','color': '#ed3f14'})
        rgb_array.append({'icon':'md-chatbubbles','color': '#E46CBB'})
        rgb_array.append({'icon':'md-map','color': '#9A66E4'})
        for index,value in enumerate(queryset):
            obj = {}
            total_num+=value.num
            obj['title'] = Company.objects.get(id=value.company_id).name
            obj['count'] = value.num
            obj['icon']  = rgb_array[index].get("icon")
            obj['color']  = rgb_array[index].get("color")

            temp_array.append(obj)

        temp_array_total = []#临时数组
        temp_array_total.append({'title':'总设备数','count':total_num,'icon':'md-person-add','color': '#2d8cf0'})
        result['top'] = temp_array_total + temp_array

        #center left data slaveDeviceStatistic
        slave_datas = SlaveDeviceStatistic.objects.filter(created_at__gte=str(formate_time))
        result['center_left']=[]
        for slave in slave_datas:
            item = {}
            item['name'] = Slave.objects.get(id=slave.slave_id).mac
            item['value'] = slave.num
            result['center_left'].append(item)

        return Response(data=self.get_return_result(self,status.HTTP_200_OK,result,'success'))
    '''
    封装返回格式
    '''
    @staticmethod
    def get_return_result(self,code,data,msg):
        result_data = {'code': code, 'data': data, 'msg': msg}
        return result_data

class BrandTrendView(APIView):
    """
        get:

        >  品牌趋势接口

        - `设置校验位: ` http://47.93.181.56:5081//datastatistic/brand_trend
    """
    def get(self, request, *args, **kwargs):
        print('12222333')
        # queryset = CompanyDeviceStatistic.objects.all()
        # serializer_class = CompanyDeviceStatisticSerializer(queryset,many=True)
        return Response(status.HTTP_200_OK)
