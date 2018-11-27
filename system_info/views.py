from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import Brand,Company, ChannelType
from .serializers import CompanySerializer,BrandSerializer
from .serializers import ChNameCreateSerializer

# Create your views here.

class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer




class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ChCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin,
                   mixins.ListModelMixin):
    queryset = ChannelType.objects.all()
    serializer_class = ChNameCreateSerializer
