from django.contrib import admin

# Register your models here.
from .models import ChannelType, ChannelName

admin.site.register(ChannelType)
admin.site.register(ChannelName)
