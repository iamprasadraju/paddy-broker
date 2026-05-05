from django import forms


class FarmerForm(forms.Form):
    farmer_name = forms.CharField(max_length=100)
    mobile_num = forms.CharField(max_length=10)
    paddy_variety = forms.CharField(max_length=100)
    moisture = forms.DecimalField(max_digits=5, decimal_places=2)
    # Using DateInput widget to match a date picker in HTML
    date_moisture_measured = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
