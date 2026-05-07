# admin.py
from django.contrib import admin
from .models import FarmerTicket, FarmerConsignmentInfo, GovtPaddyRate, WorkersGroup, VehicleInfo, Workers

admin.site.register(FarmerTicket)
admin.site.register(FarmerConsignmentInfo)
admin.site.register(GovtPaddyRate)
admin.site.register(VehicleInfo)

@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile_num']
    search_fields = ['name', 'mobile_num']

@admin.register(WorkersGroup)
class WorkersGroupAdmin(admin.ModelAdmin):
    list_display = ['group_leader']
    search_fields = ['group_leader__name', 'group_members__name']
    filter_horizontal = ['group_members']

