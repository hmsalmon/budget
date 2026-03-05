from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, BillingCycle
from .forms import TransactionForm

def index(request):
    return render(request, 'core/index.html')

def dashboard(request):

    #transactions = Transaction.objects.select_related('billing_cycle').all().order_by('date')

    try:
        sel_cycle = request.GET.get('sel_cycle',"1") or request.POST.get('sel_cycle',"1")
        sel_cycle = int(sel_cycle)
    except (TypeError, ValueError):
        sel_cycle = 1

    transactions = Transaction.objects.select_related('billing_cycle').filter(billing_cycle_id = sel_cycle).order_by('date')

    total_income = sum(t.amount for t in transactions if t.transaction_type == 'IN')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'EX')
    balance = total_income - total_expense

    billingCycles = BillingCycle.objects.all().order_by('startDate')#filter(id = sel_cycle)#values_list('displayName', flat=True).distinct()#Transaction.objects.select_related('billing_cycle')#.distinct() #.values_list('billing_cycle_id', flat=True)

    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        print(form.errors)
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

    bc = BillingCycle.objects.order_by("endDate")

    context = {
        'billingCycles': bc
    }

    return render(request, 'core/overview.html',context)