from django.urls import path
from . import views

#urls.py as address for routing

app_name = 'tracker'

urlpatterns = [
    path('',  views.dashboard, name = 'dashboard',)
]