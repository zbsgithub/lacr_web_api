from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Brand,Company, StdChName, AliasChName
from .serializers import CompanySerializer, BrandSerializer, StdChSerializer, AliasChSerializer
from .filter import AliasChFilters, StdChFilters


class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class StdChViewSet(viewsets.ModelViewSet):
    queryset = StdChName.objects.all()
    serializer_class = StdChSerializer
    filter_class = StdChFilters


class AliasChViewSet(viewsets.ModelViewSet):
    queryset = AliasChName.objects.all()
    serializer_class = AliasChSerializer
    filter_class = AliasChFilters


