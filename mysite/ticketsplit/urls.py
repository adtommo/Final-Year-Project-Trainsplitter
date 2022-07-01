from django.urls import path

from . import views

urlpatterns = [
path("", views.index, name="index"),
path("index/", views.index, name="index"),
path("whataresplit/", views.whataresplit, name="whataresplit"),
path("howtousesplit/", views.howtousesplit, name="howtousesplit"),
]

