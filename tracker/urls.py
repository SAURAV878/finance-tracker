from django.urls import path
from . import views

#urls.py as address for routing

app_name = 'tracker'

urlpatterns = [
    path('',  views.dashboard, name = 'dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('transaction/<int:pk>/edit/', views.edit_transaction, name='edit_transaction'),
]