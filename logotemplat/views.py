from rest_framework import viewsets, mixins
from .serializers import LogoTemplateSerializer
from .models import LogoTemplate
from .filter import LogoTempFilters


class LogoTempView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = LogoTemplateSerializer
    queryset = LogoTemplate.objects.all()
    filter_class = LogoTempFilters

    @staticmethod
    def get_machine_list(queryset):
        return queryset.values_list("machine")

    def get_queryset(self):
        machine_list = int(self.request.query_params.get("machine_list", 0))
        if machine_list == 1:
            self.get_machine_list(self.queryset)
