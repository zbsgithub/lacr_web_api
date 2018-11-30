from django.contrib import admin
from .models import ChannelType, ChannelName, Slave, Company, Brand


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias", "created_at", "updated_at", )
admin.site.register(Company, CompanyAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias", "company", "created_at", "updated_at", )
admin.site.register(Brand, BrandAdmin)


class ChannelTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias")
admin.site.register(ChannelType, ChannelTypeAdmin)


class ChannelNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias", "chid", "classify", "image")
admin.site.register(ChannelName, ChannelNameAdmin)


class SlaveAdmin(admin.ModelAdmin):
    list_display = ("id", "mac", "created_at", "created_at", )
admin.site.register(Slave, SlaveAdmin)

