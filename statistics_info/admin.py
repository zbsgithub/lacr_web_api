from django.contrib import admin
from .models import CompanyDeviceStatistic, BrandDeviceStatistic, SlaveDeviceStatistic, \
    CompanyImgStatistic, BrandImgStatistic


class CompanyDeviceStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "num", "created_at", )
admin.site.register(CompanyDeviceStatistic, CompanyDeviceStatisticAdmin)


class BrandDeviceStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "num", "created_at", )
admin.site.register(BrandDeviceStatistic, BrandDeviceStatisticAdmin)


class SlaveDeviceStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "slave", "num", "created_at", )
admin.site.register(SlaveDeviceStatistic, SlaveDeviceStatisticAdmin)


class CompanyImgStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "num", "created_at", )
admin.site.register(CompanyImgStatistic, CompanyImgStatisticAdmin)


class BrandImgStatisticAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "num", "created_at", )
admin.site.register(BrandImgStatistic, BrandImgStatisticAdmin)
