from django import forms
from django import forms
from django.contrib.auth.models import User # Import User model
from django.contrib.auth.forms import UserCreationForm # Import UserCreationForm
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    # Override the category field to filter by user's categories only
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Use all categories
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'type': 'Type',
            'category': 'Category',
            'amount': 'Amount',
            'date': 'Date',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # Pop the 'user' argument
        super().__init__(*args, **kwargs)

        # Add Bootstrap-like classes for basic styling to other fields
        for field_name, field in self.fields.items():
            if field_name != 'category': # Category widget already set
                if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Textarea, forms.Select)):
                    field.widget.attrs.update({'class': 'form-control'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Category Name',
            'type': 'Category Type',
        }


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'