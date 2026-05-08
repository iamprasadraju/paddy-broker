# admin.py
from django.contrib import admin
from .models import FarmerTicket, FarmerConsignmentInfo, WorkersGroup, VehicleInfo, Workers, AdminSettings, AdminDashboard, PaddyInfo
from django.db.models import Sum, F


admin.site.register(FarmerTicket)
admin.site.register(VehicleInfo)
admin.site.register(PaddyInfo)

@admin.register(FarmerConsignmentInfo)
class FarmerConsignmentInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('total_brokerage',)


@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile_num']
    search_fields = ['name', 'mobile_num']

@admin.register(WorkersGroup)
class WorkersGroupAdmin(admin.ModelAdmin):
    list_display = ['group_leader']
    search_fields = ['group_leader__name', 'group_members__name']
    filter_horizontal = ['group_members']


@admin.register(AdminSettings)
class AdminSettingsAdmin(admin.ModelAdmin):
    # This prevents anyone from adding a NEW object
    def has_add_permission(self, request):
        return False

    # This prevents anyone from deleting the existing settings object
    def has_delete_permission(self, request, obj=None):
        return False

    # Optional: If you want to make sure the "Add" button doesn't show 
    # even if the database is empty (forces you to use a migration or shell to create the first one)
    def has_add_permission(self, request):
        if AdminSettings.objects.exists():
            return False
        return True

@admin.register(AdminDashboard)
class AdminDashboardAdmin(admin.ModelAdmin):
    change_list_template = 'admin/analytics_dashboard.html'

    def changelist_view(self, request, extra_context=None):
        # 1. Calculate totals
        total_worker_fees = FarmerConsignmentInfo.objects.aggregate(Sum('total_brokerage'))['total_brokerage__sum'] or 0
        total_bags = FarmerConsignmentInfo.objects.aggregate(Sum('num_bags'))['num_bags__sum'] or 0

        # 2. Revenue calculation (Weight in 75kg units * Paddy Rate)
        # We join through tracking_id to get the PaddyVariety and its rate
        revenue_data = FarmerConsignmentInfo.objects.annotate(
            rate=F('tracking_id__paddy_variety__paddy_rate')
        ).aggregate(
            total_rev=Sum(F('num_bags') * 40 / 75 * F('rate'))
        )
        total_revenue = revenue_data['total_rev'] or 0

        # 3. Profit
        profit = total_revenue - total_worker_fees

        # 4. Inject into context
        extra_context = extra_context or {}
        extra_context['stats'] = {
            'total_bags': total_bags,
            'worker_fees': total_worker_fees,
            'revenue': total_revenue,
            'profit': profit,
        }
        extra_context['title'] = "Real-time Business Analytics" # Changes the page heading

        return super().changelist_view(request, extra_context=extra_context)