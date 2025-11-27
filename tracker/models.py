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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
