# admin.py
from django.contrib import admin
from .models import FarmerTicket, FarmerConsignmentInfo

admin.site.register(FarmerTicket)
admin.site.register(FarmerConsignmentInfo)
