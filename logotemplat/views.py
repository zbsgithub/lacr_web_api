from rest_framework import viewsets, mixins
from .serializers import LogoTemplateSerializer, MachineListSerializer
from .models import LogoTemplate
from .filter import LogoTempFilters


class LogoTempView(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.UpdateModelMixin):
    """
    list:

    > 台标特征列表

    - `所有设备列表: ` http://47.93.181.56:5081/logotemplat/template/?machine_list=1

    - `指定设备的特征: ` http://47.93.181.56:5081/logotemplat/template/?machine=设备名字

    - `状态码: `: 200


    """
    serializer_class = LogoTemplateSerializer
    queryset = LogoTemplate.objects.all()
    filter_class = LogoTempFilters

    @staticmethod
    def get_machine_list(queryset):
        return queryset.values_list("machine").values("machine")

    def get_serializer_class(self):
        machine_list = int(self.request.query_params.get("machine_list", 0))
        if machine_list == 1:
            return MachineListSerializer
        else:
            return LogoTemplateSerializer

    def get_queryset(self):
        machine_list = int(self.request.query_params.get("machine_list", 0))
        if machine_list == 1:
            self.get_machine_list(self.queryset)


