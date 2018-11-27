from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from .models import Brand,Company, ChannelType
from .serializers import CompanySerializer,BrandSerializer
from .serializers import ChNameCreateSerializer
from rest_framework.response import Response

# Create your views here.

class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer




class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ChCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ChannelType.objects.all()
    serializer_class = ChNameCreateSerializer

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
