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
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'frequency': forms.NumberInput(attrs={'placeholder': 'e.g. 1'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }