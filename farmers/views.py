from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from .forms import FarmerForm


def home(request):
    return render(request, "farmers/index.html")


# Book tickets by farmers for packing paddy
def book_ticket(request):
    if request.method == "POST":
        form = FarmerForm(request.POST)
        if form.is_valid():
            return HttpResponse("thanks")
    else:
        form = FarmerForm()

    return render(request, "farmers/book_ticket.html", {"form": form})
