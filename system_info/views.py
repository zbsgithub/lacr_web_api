from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Brand,Company
from .serializers import CompanySerializer,BrandSerializer

# Create your views here.

class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer




class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer