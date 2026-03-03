from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, BillingCycle
from .forms import TransactionForm

def index(request):
    return render(request, 'core/index.html')

def dashboard(request):

    transactions = Transaction.objects.all().order_by('date')

    # sel_cycle = "Dec25"
    # if request.method == 'GET':
    #     sel_cycle = request.GET.get('sel_cycle','Dec25')
    
    # transactions = transactions.filter(billing_cycle=1)

    total_income = sum(t.amount for t in transactions if t.transaction_type == 'IN')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'EX')
    balance = total_income - total_expense

    billingCycles = Transaction.objects.values_list('billing_cycle_id', flat=True).distinct()

    # if request.method == 'POST':
    #     form = TransactionForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('dashboard')
    # else:
    #     form = TransactionForm()

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'billingCycles': billingCycles,
        'form': TransactionForm(),
        'selected_cycle': 1
    }
    return render(request, 'core/dashboard.html', context)

def overview(request):

    bc = BillingCycle.objects.order_by("endDate")

    context = {
        'billingCycles': bc
    }

    return render(request, 'core/overview.html',context)