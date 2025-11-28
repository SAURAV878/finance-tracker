from django.shortcuts import render, redirect, get_object_or_404 # Import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm

# Create your views here.
@login_required
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

@login_required
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

@login_required
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

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('tracker:dashboard')
    
    return render(request, 'tracker/transaction_confirm_delete.html', {'transaction': transaction})



