from django.contrib import admin
from .models import CompanyDeviceStatistic, BrandDeviceStatistic, SubordinateDeviceStatistic, \
    CompanyImgStatistic, BrandImgStatistic


class CompanyDeviceStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "num", "created_at", )
admin.site.register(CompanyDeviceStatistic, CompanyDeviceStatisticAdmin)


class BrandDeviceStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "num", "created_at", )
admin.site.register(BrandDeviceStatistic, BrandDeviceStatisticAdmin)


class SubordinateDeviceStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "subordinate", "num", "created_at", )
admin.site.register(SubordinateDeviceStatistic, SubordinateDeviceStatisticAdmin)


class CompanyImgStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "num", "created_at", )
admin.site.register(CompanyImgStatistic, CompanyImgStatisticAdmin)


class BrandImgStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "num", "created_at", )
admin.site.register(BrandImgStatistic, BrandImgStatisticAdmin)
