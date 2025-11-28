from django.shortcuts import render
from django.db.models import Sum
from .models import Transaction

# Create your views here.
# views = handle requets and response of function

def dashboard(request):#request = object conating info about HTTP request
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(type = 'income').aaggregate(Sum('amount')) ['amount__sum'] or 0
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