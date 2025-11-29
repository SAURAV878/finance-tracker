from django import forms
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

    def __init__(self, *args, **kwargs):
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
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Category Name',
            'type': 'Category Type',
        }


