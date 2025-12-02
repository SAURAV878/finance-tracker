from django.contrib import admin
from .models import Category, Transaction

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction)
