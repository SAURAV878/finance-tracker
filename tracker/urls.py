from django.urls import path
from . import views

#urls.py as address for routing

app_name = 'tracker'

urlpatterns = [
    path('',  views.welcome_page, name = 'welcome_page'), # New welcome page at root
    path('dashboard/',  views.dashboard, name = 'dashboard'), # Dashboard moved to /dashboard/
    path('register/', views.register, name='register'), # New register URL
    path('add/', views.add_transaction, name='add_transaction'),
    path('transaction/<int:pk>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transaction/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
