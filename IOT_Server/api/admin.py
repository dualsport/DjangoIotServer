#--- IOT_Server - api app -----------------------------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

from django.contrib import admin
from api.models import Devices, Tags, ValueTypes

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'name')
    readonly_fields = ('created_on', 'updated_on',)
admin.site.register(Devices, DeviceAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'name', 'device_concat')
    readonly_fields = ('created_on', 'updated_on',)
admin.site.register(Tags, TagAdmin)

class ValueTypeAdmin(admin.ModelAdmin):
    list_display = ('value_type_id', 'name')
    readonly_fields = ('created_on', 'updated_on',)
admin.site.register(ValueTypes, ValueTypeAdmin)