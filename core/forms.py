from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title','date', 'amount', 'transaction_type', 'category', 'notes']