from django import forms
from .models import Transaction, Category
from django.contrib.auth.forms import UserCreationForm # Import UserCreationForm
from django.contrib.auth.models import User

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'amount', 'type', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']
