from django.contrib import admin
from .models import StdChName, AliasChName, Slave, Company, Brand


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias", "created_at", "updated_at", )
admin.site.register(Company, CompanyAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "alias", "company", "created_at", "updated_at", )
admin.site.register(Brand, BrandAdmin)


class StdChNameAdmin(admin.ModelAdmin):
    list_display = ("id", "ch_id", "name", "image", "created_at", "updated_at", )
admin.site.register(StdChName, StdChNameAdmin)


class AliasChNameAdmin(admin.ModelAdmin):
    list_display = ("id", "std_ch", "name", "created_at", "updated_at", )
admin.site.register(AliasChName, AliasChNameAdmin)


class SlaveAdmin(admin.ModelAdmin):
    list_display = ("id", "mac", "created_at", "created_at", )
admin.site.register(Slave, SlaveAdmin)

