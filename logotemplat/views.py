from rest_framework import viewsets, mixins
from .serializers import LogoTemplateSerializer
from .models import LogoTemplate
from .filter import LogoTempFilters


class LogoTempView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = LogoTemplateSerializer
    queryset = LogoTemplate.objects.all()
    filter_class = LogoTempFilters
