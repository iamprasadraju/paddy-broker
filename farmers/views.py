from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from .forms import FarmerForm
from .models import FarmerTicket


def home(request):
    farmers = FarmerTicket.objects.all()
    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id")
        if ticket_id:
            farmer = FarmerTicket.objects.get(tracking_id=ticket_id)
            return render(request, "farmers/track_ticket.html", {"farmer": farmer})
    return render(request, "farmers/index.html", {"farmers": farmers})


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


