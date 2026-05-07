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
    paddy_variety = models.ForeignKey('GovtPaddyRate', on_delete=models.CASCADE, verbose_name="Paddy Variety")
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
            self.created_at = timezone.now()

            # 3. Combine them: VIJA-AF32 (if location was Vijayawada)
            self.tracking_id = f"{loc_prefix}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_id} ({self.farmer_name})"


class FarmerConsignmentInfo(models.Model):
    # One-to-one relationship with FarmerTicket
    tracking_id = models.OneToOneField(FarmerTicket, on_delete=models.CASCADE, limit_choices_to={'status': FarmerTicket.Status.PACKED})
    num_bags = models.IntegerField(verbose_name="Number of bags (40 kg)")
    brokerage_per_bag = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Brokerage per bag (75 kg)")
    total_brokerage = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="Total Brokerage (calculated)")
    workers_group = models.ForeignKey('WorkersGroup', on_delete=models.CASCADE, verbose_name="Workers Group", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vehicle = models.OneToOneField('VehicleInfo', on_delete=models.CASCADE, verbose_name="Vehicle", null=True, blank=True)
    consignment_created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Consignment Created By")

    def save(self, *args, **kwargs):
        self.total_brokerage = self.num_bags * 40 / 75 * self.brokerage_per_bag
        super().save(*args, **kwargs)


class GovtPaddyRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Government Rate")
    paddy_variety = models.CharField(max_length=100, verbose_name="Paddy Variety")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.paddy_variety} - {self.rate} per 75kg"


class VehicleInfo(models.Model):
    vehicle_number = models.CharField(max_length=100, verbose_name="Vehicle Number")
    driver_name = models.CharField(max_length=100, verbose_name="Driver Name")
    driver_contact = models.CharField(max_length=100, verbose_name="Driver Contact")

class Workers(models.Model):
    name = models.CharField(max_length=100, verbose_name="Worker Name")
    mobile_num = models.CharField(max_length=10, verbose_name="Mobile Number")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class WorkersGroup(models.Model):
    group_leader = models.ForeignKey('Workers', on_delete=models.CASCADE, verbose_name="Group Leader", related_name='led_groups')
    group_members = models.ManyToManyField('Workers', verbose_name="Group Members", blank=True, related_name='member_of_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.group_leader.name} - {self.group_members.count()} members"