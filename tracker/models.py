from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Category(models.Model):
    CATEGORY_TYPES =  [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.type})"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date  = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class META:
        ordering = ['-date', '-created_at'] #- means keep in descending, newset frist

    def __str__(self):
        return f"{self.type} - ${self.amount} - {self.date}" #define how trans apperas in admin panel.
