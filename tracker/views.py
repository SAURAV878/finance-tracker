from django.shortcuts import render
from .models import Transaction

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})