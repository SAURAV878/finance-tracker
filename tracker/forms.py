from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'description', 'amount', 'type', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
