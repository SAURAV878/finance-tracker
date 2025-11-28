from django.shortcuts import render, redirect # Import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, Category # Import Category model
from .forms import TransactionForm # Import our new form

# Create your views here.
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(type = 'income').aggregate(Sum('amount')) ['amount__sum'] or 0
    total_expense = transactions.filter(type = 'expense').aggregate(Sum('amount')) ['amount__sum'] or 0

    balance = total_income - total_expense
    recent_transactions = transactions[:5]

    context = {
        'total_income' : total_income,
        'total_expense' : total_expense,
        'balance' : balance,
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
            return redirect('tracker:dashboard') # Redirect to the dashboard after saving
    else:
        form = TransactionForm(user=request.user) # Pass the user to filter categories
    
    return render(request, 'tracker/transaction_form.html', {'form': form, 'title': 'Add Transaction'})



