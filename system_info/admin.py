from django.contrib import admin
from .models import ChannelType, ChannelName, Slave


class ChannelTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias")
admin.site.register(ChannelType, ChannelTypeAdmin)


class ChannelNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias", "chid", "classify", "image")
admin.site.register(ChannelName, ChannelNameAdmin)


class SlaveAdmin(admin.ModelAdmin):
    list_display = ("id", "mac", "created_at", "created_at", )
admin.site.register(Slave, SlaveAdmin)

