from django import forms
from django.contrib.auth.models import User # Import User model
from django.contrib.auth.forms import UserCreationForm # Import UserCreationForm
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    # Override the category field to filter by user's categories only
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),  # Start with an empty queryset
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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

    def __init__(selfself, *args, **kwargs):
        user = kwargs.pop('user', None) # Pop the 'user' argument
        super().__init__(*args, **kwargs)

        # Filter categories based on the user
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')

        # Add Bootstrap-like classes for basic styling to other fields
        for field_name, field in self.fields.items():
            if field_name != 'category': # Category widget already set
                if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Textarea, forms.Select)):
                    field.widget.attrs.update({'class': 'form-control'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'user'] # Added 'user' field
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}), # Added widget for user
        }
        labels = {
            'name': 'Category Name',
            'type': 'Category Type',
            'user': 'Owner', # Added label for user
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None) # Get the current logged-in user
        super().__init__(*args, **kwargs)

        # If the user is not a superuser, restrict the 'user' field to only the current user
        if current_user and not current_user.is_superuser:
            self.fields['user'].queryset = User.objects.filter(pk=current_user.pk)
            self.fields['user'].initial = current_user
            self.fields['user'].disabled = True # Make it read-only
            self.fields['user'].widget.attrs['readonly'] = True # Add readonly attribute for styling/JS
        else:
            # For superusers, allow selection of all users
            self.fields['user'].queryset = User.objects.all().order_by('username')

        # Set default styling for all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Select)):
                field.widget.attrs.update({'class': 'form-control'})

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'