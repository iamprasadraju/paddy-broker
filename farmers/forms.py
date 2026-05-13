# forms.py
from django import forms

from .models import FarmerTicket


class FarmerForm(forms.ModelForm):
    class Meta:
        model = FarmerTicket
        # List the fields you want to show in the form
        fields = [
            "farmer_name",
            "mobile_num",
            "aadhar_num",
            "location",
            "paddy_variety",
            "moisture",
            "date_moisture_measured",
        ]
        # Keep your date picker widget
        widgets = {
            "farmer_name": forms.TextInput(attrs={"readonly": "readonly", "placeholder": "Scan Aadhar"}),
            "aadhar_num": forms.TextInput(attrs={"readonly": "readonly", "placeholder": "Scan Aadhar"}),
            "location": forms.TextInput(attrs={"readonly": "readonly", "placeholder": "Scan Location"}),
            "date_moisture_measured": forms.DateInput(attrs={"type": "date"}),
        }
    