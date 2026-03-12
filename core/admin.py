from django.contrib import admin
from .models import Transaction, BillingCycle, Date

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'transaction_type', 'category', 'date')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('title', 'category', 'notes')

@admin.register(BillingCycle)
class BillingCycleAdmin(admin.ModelAdmin):
    list_display = ('fullName', 'startDate', 'endDate','dueDate')
    list_filter = ('fullName','code','displayName', 'startDate', 'endDate','dueDate')

@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ('date', 'isWeekend')
    list_filter = ('date','day','month', 'year', 'week','monthName','weekdayName', 'isWeekend')