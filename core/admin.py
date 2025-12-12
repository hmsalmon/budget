from django.contrib import admin
from .models import Transaction, BillingCycle

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'transaction_type', 'category', 'date')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('title', 'category', 'notes')

@admin.register(BillingCycle)
class BillingCycleAdmin(admin.ModelAdmin):
    list_display = ('fullName', 'startDate', 'endDate')
    list_filter = ('fullName','code','displayName', 'startDate', 'endDate','dueDate')