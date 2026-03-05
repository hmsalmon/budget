from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone as tz
from django.db.models import Sum, Count
from .models import Transaction, BillingCycle
from .forms import TransactionForm

def index(request):
    return render(request, 'core/index.html')

def dashboard(request):

    #transactions = Transaction.objects.select_related('billing_cycle').all().order_by('date')

    billingCycles = BillingCycle.objects.all().order_by('startDate')
    current_bill_cycle = billingCycles.filter(endDate__gte = '2026-03-05').first()

    try:
        sel_cycle = request.GET.get('sel_cycle',current_bill_cycle.id) or request.POST.get('sel_cycle',current_bill_cycle.id)
        sel_cycle = int(sel_cycle)
    except (TypeError, ValueError):
        sel_cycle = current_bill_cycle.id

    transactions = Transaction.objects.select_related('billing_cycle').filter(billing_cycle_id = sel_cycle).order_by('date')

    total_income = sum(t.amount for t in transactions if t.transaction_type == 'IN')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'EX')
    balance = total_income - total_expense


    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'billingCycles': billingCycles,
        'form': form,
        'selected_cycle': sel_cycle
    }
    return render(request, 'core/dashboard.html', context)

def overview(request):

    bc = BillingCycle.objects.order_by("endDate").annotate(
        total_amount=Sum("transactions__amount"),
        num_trans=Count("transactions__id")
    )

    context = {
        'billingCycles': bc
    }

    return render(request, 'core/overview.html',context)