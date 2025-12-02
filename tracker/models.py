from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Import User model

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Add user field

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('name', 'user') # Ensure unique categories per user

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Changed here
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.description} - {self.get_type_display()} - {self.amount}"
