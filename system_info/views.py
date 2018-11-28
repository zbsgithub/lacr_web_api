from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Brand,Company, ChannelType, ChannelName
from .serializers import CompanySerializer,BrandSerializer
from .serializers import ChNameSerializer, ChTypeSerializer, ChTypeListSerializer
from .filter import ChannelNameFilters, ChannelTypeFilters


class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer




class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ChTypeViewSet(viewsets.ModelViewSet):
    queryset = ChannelType.objects.all()
    serializer_class = ChTypeSerializer
    filter_class = ChannelTypeFilters


class ChNameViewSet(viewsets.ModelViewSet):
    queryset = ChannelName.objects.all()
    serializer_class = ChNameSerializer
    filter_class = ChannelNameFilters


class ChTypeListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ChannelType.objects.all()
    serializer_class = ChTypeListSerializer

