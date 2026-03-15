from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from django.utils import timezone as tz
from django.db.models import Sum, Count
from .models import Transaction, BillingCycle, Date, Scheduled
from .forms import TransactionForm, ScheduledForm
from django.forms import modelformset_factory
from datetime import date

def edit(request):

    TransactionFormSet = modelformset_factory(
        Transaction,
        fields=("date", "title", "amount", "category", "transaction_type", "notes"),
        extra=0
    )

    if request.method == "POST":
        formset = TransactionFormSet(request.POST)

        if formset.is_valid():
            formset.save()

    else:
        formset = TransactionFormSet()

    context = {
        "formset": formset
    }

    return render(request, 'core/edit.html', context)

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

    year_choices = Date.objects.filter(year__gte = 2025).values_list("year", flat=True).distinct()


    current_year = date.today().year
    try:
        sel_year = request.GET.get('sel_year',current_year) or request.POST.get('sel_year',current_year)
        sel_year = int(sel_year)
    except (TypeError, ValueError):
        sel_year = current_year

    #date = Date.objects.select_related("transactions").filter(year = sel_year).order_by("date")

    trans_bymonth = Transaction.objects.filter(date__year = sel_year)
    
    #Date.objects.filter(year = sel_year).


    bc = BillingCycle.objects.filter(
        endDate__gte = date(sel_year,1,1),
        endDate__lte = date(sel_year + 1,1,1)
        ).order_by("endDate"
        ).annotate(
            total_amount=Sum("transactions__amount"),
            num_trans=Count("transactions__id")
    )

    context = {
        'years' : year_choices,
        'selected_year': sel_year,
        'billingCycles': bc
    }

    return render(request, 'core/overview.html',context)

def scheduled(request):

    sched_list = Scheduled.objects.all()

    form = ScheduledForm()
    if request.method == 'POST':
        form = ScheduledForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scheduled')
    else:
        form = ScheduledForm()


    context = {
        'schedules': sched_list,
        'form': form
    }

    return render(request, 'core/scheduled.html', context)
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction.title = data.get('title', transaction.title)
        transaction.amount = data.get('amount', transaction.amount)
        transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
        transaction.category = data.get('category', transaction.category)
        transaction.notes = data.get('notes', transaction.notes)
        date_val = data.get('date')
        if date_val:
            try:
                date_obj = Date.objects.get(date=date_val)
                transaction.date = date_obj
            except Date.DoesNotExist:
                return JsonResponse({'error': f'Date {date_val} not found in database'}, status=400)
        transaction.save()
        return JsonResponse({
            'success': True,
            'date': str(transaction.date_id),
            'title': transaction.title,
            'transaction_type': transaction.transaction_type,
            'transaction_type_display': transaction.get_transaction_type_display(),
            'category': transaction.category,
            'amount': str(transaction.amount),
            'notes': transaction.notes,
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)
