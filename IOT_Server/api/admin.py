from django.contrib import admin
from api.models import Devices, Tags, ValueTypes

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'name', )
admin.site.register(Devices, DeviceAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', 'name', 'device_concat')
admin.site.register(Tags, TagAdmin)

class ValueTypeAdmin(admin.ModelAdmin):
    list_display = ('value_type_id', 'name')
admin.site.register(ValueTypes, ValueTypeAdmin)