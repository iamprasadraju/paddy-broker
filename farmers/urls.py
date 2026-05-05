from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book_ticket/", views.book_ticket, name="book_ticket"),
]
