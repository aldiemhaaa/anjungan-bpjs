
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('cetaksep/',views.cetakSep),
    path('cetaksep/pilihdokter/',views.pilihDokter)
]
