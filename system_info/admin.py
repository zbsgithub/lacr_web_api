from django.contrib import admin
from .models import ChannelType, ChannelName


class ChannelTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias")
admin.site.register(ChannelType, ChannelTypeAdmin)


class ChannelNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias", "classify__name")
admin.site.register(ChannelName, ChannelNameAdmin)
