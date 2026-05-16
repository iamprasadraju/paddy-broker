import uuid

from django.db import models
from django.utils import timezone


class FarmerTicket(models.Model):
    class Status(models.TextChoices):
        TICKET_BOOKED = "Ticket Booked"
        ONGOING = "Ongoing"
        PACKED = "Packed"
        PICKED = "Picked"
        TRANSPORTED = "Transported"

    priority = models.AutoField(primary_key=True, verbose_name="Priority")
    tracking_id = models.CharField(max_length=50, unique=True, editable=False, verbose_name="Tracking ID")
    farmer_name = models.CharField(max_length=100, verbose_name="Farmer Name")
    mobile_num = models.CharField(max_length=10, verbose_name="Mobile Number")
    aadhar_num = models.CharField(max_length=12, verbose_name="Aadhar Number")
    location = models.CharField(max_length=100, verbose_name="Location")
    paddy_variety = models.ForeignKey('PaddyInfo', on_delete=models.CASCADE, verbose_name="Paddy Variety")
    moisture = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Moisture")
    date_moisture_measured = models.DateField(verbose_name="Date Moisture Measured")
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.TICKET_BOOKED, verbose_name="Status")

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # 1. Get the first 4 letters of location and make them UPPERCASE
            # We use [:4] to slice the string and .upper() for capitals
            loc_prefix = self.location[:4].upper()

            # 2. Generate a random unique suffix (e.g., 4 characters)
            unique_suffix = uuid.uuid4().hex[:6].upper()

            # 3. Combine them: VIJA-AF32 (if location was Vijayawada)
            self.tracking_id = f"{loc_prefix}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_id} ({self.farmer_name})"


class FarmerConsignmentInfo(models.Model):
    # One-to-one relationship with FarmerTicket
    tracking_id = models.OneToOneField(FarmerTicket, on_delete=models.CASCADE, limit_choices_to={'status': FarmerTicket.Status.ONGOING})
    num_bags = models.IntegerField(verbose_name="Number of bags (40 kg)")
    workers_group = models.ForeignKey('WorkersGroup', on_delete=models.CASCADE, verbose_name="Workers Group", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vehicle = models.OneToOneField('VehicleInfo', on_delete=models.CASCADE, verbose_name="Vehicle", null=True, blank=True)
    consignment_created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Consignment Created By")

    total_brokerage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Brokerage", default=0)

    def save(self, *args, **kwargs):
        if self.workers_group:
            # We recalculate every time, overwriting any manual input
            self.total_brokerage = (self.num_bags * 40 / 75) * self.workers_group.worker_group_fee_per_bag
            
        super().save(*args, **kwargs)

class PaddyInfo(models.Model):
    paddy_variety = models.CharField(max_length=100, verbose_name="Paddy Variety")
    paddy_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Government Rate per 75kg")

    def __str__(self):
        return f"{self.paddy_variety} - {self.paddy_rate} per 75kg"


class VehicleInfo(models.Model):
    vehicle_number = models.CharField(max_length=100, verbose_name="Vehicle Number")
    driver_name = models.CharField(max_length=100, verbose_name="Driver Name")
    driver_contact = models.CharField(max_length=100, verbose_name="Driver Contact")

class Workers(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        INACTIVE = 'Inactive', 'Inactive'
    
    name = models.CharField(max_length=100, verbose_name="Worker Name")
    mobile_num = models.CharField(max_length=10, verbose_name="Mobile Number")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class WorkersGroup(models.Model):
    group_leader = models.ForeignKey('Workers', on_delete=models.CASCADE, verbose_name="Group Leader", related_name='led_groups')
    group_members = models.ManyToManyField('Workers', verbose_name="Group Members", blank=True, related_name='member_of_groups')
    
    # when bags are packed and enter by group leader, group revenue is calculated automatically from (worker_group_fee_per_bag * number_of_bags (75kgs))
    group_revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Group Revenue", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.group_leader.name} - {self.group_members.count()} members"

# class for broker to track whats actually happening whole management (ex: profit, loss, workerspay, etc)
class AdminSettings(models.Model):
    workers_group_fee_per_bag = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Workers Group Fee Per Bag", default=0)
    mill_fee_per_bag = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Mill Fee Per Bag", default=0)

    def __str__(self):
        return "Admin custom modifications"
        
class AdminDashboard(AdminSettings):
    class Meta:
        proxy = True
        verbose_name = "Business Analytics"
        verbose_name_plural = "Business Analytics"