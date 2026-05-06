from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from .forms import FarmerForm
from .models import FarmerTicket, FarmerConsignmentInfo


def home(request):
    # Get all farmers with their consignment info in one query
    farmers = FarmerTicket.objects.all()
    consignment_info = FarmerConsignmentInfo.objects.all()
    farmer_metadata = [col.verbose_name for col in farmers.model._meta.fields]
    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id")
        if ticket_id:
            farmer = FarmerTicket.objects.get(tracking_id=ticket_id) and FarmerConsignmentInfo.objects.get(tracking_id=ticket_id)
            return render(request, "farmers/track_ticket.html", {"farmer": farmer}, {"consignment": consignment_info})
    return render(request, "farmers/index.html", {"pending_farmers": farmers.exclude(status=FarmerTicket.Status.TRANSPORTED), "happy_farmers": farmers.filter(status=FarmerTicket.Status.TRANSPORTED), "farmer_metadata": farmer_metadata}) # pending farmers are who status is not TRANSPORTED


# Book tickets by farmers for packing paddy
def book_ticket(request):
    if request.method == "POST":
        form = FarmerForm(request.POST)
        if form.is_valid():
            ticket = form.save()

            return HttpResponse("thanks")
    else:
        form = FarmerForm()

    return render(request, "farmers/book_ticket.html", {"form": form})


