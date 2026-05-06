import uuid

from django.db import models


class FarmerTicket(models.Model):
    tracking_id = models.CharField(max_length=50, unique=True, editable=False)
    farmer_name = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    paddy_variety = models.CharField(max_length=100)
    moisture = models.DecimalField(max_digits=5, decimal_places=2)
    date_moisture_measured = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # 1. Get the first 4 letters of location and make them UPPERCASE
            # We use [:4] to slice the string and .upper() for capitals
            loc_prefix = self.location[:4].upper()

            # 2. Generate a random unique suffix (e.g., 4 characters)
            unique_suffix = uuid.uuid6().hex[:4].upper()

            # 3. Combine them: VIJA-AF32 (if location was Vijayawada)
            self.tracking_id = f"{loc_prefix}-{unique_suffix}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_id} ({self.farmer_name})"
