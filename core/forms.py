from django import forms
from .models import Transaction, Scheduled

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title','date', 'amount', 'transaction_type', 'category', 'notes']

class ScheduledForm(forms.ModelForm):
    class Meta:
        model = Scheduled
        fields = ['name', 'frequency', 'period', 'amount', 'type', 'startDate', 'endDate']