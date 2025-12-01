from django.shortcuts import render, redirect, get_object_or_404 # Import get_object_or_404
from django.urls import reverse# Import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm, UserRegisterForm # Import UserRegisterForm
from django.contrib import messages # Import messages




# Create your views here.

def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_income - total_expense
    recent_transactions = transactions.order_by('-date', '-created_at')[:5] # Ensure consistent ordering

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'tracker/dashboard.html', context)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('tracker:dashboard')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Add Transaction'})

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tracker:dashboard')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Edit Transaction'})


def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('tracker:dashboard')
    
    return render(request, 'tracker/transaction_confirm_delete.html', {'transaction': transaction})
@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, 'tracker/category_list.html', {'categories': categories, 'title': 'Manage Categories'})

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False) # Commit=False to set user before saving
            category.user = request.user       # Add back this line
            category.save()
            return redirect('tracker:category_list')
    else:
        form = CategoryForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Add Category',
        'action_url': reverse('tracker:category_add')
    }
    return render(request, 'tracker/category_form.html', context)
@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tracker:category_list')
    else:
        form = CategoryForm(instance=category, user=request.user)
    
    context = {
        'form': form,
        'title': 'Edit Category',
        'action_url': reverse('tracker:category_edit', kwargs={'pk': pk})
    }
    return render(request, 'tracker/category_form.html', context)
@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('tracker:category_list')
    return render(request, 'tracker/category_confirm_delete.html', {'category': category, 'title': 'Delete Category'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in.')
            return redirect('login') # Redirect to login page
    else:
        form = UserRegisterForm()
    return render(request, 'tracker/register.html', {'form': form})


def welcome_page(request):
    return render(request, 'tracker/welcome.html')
