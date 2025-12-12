from django.db import models
from datetime import date
#from core.utils import date_to_billingcycle

class BillingCycle(models.Model):

    code = models.CharField(max_length=5, unique = True)
    fullName = models.CharField(max_length=14, unique = True)
    displayName = models.CharField(max_length=24,null=True, unique = True)
    startDate = models.DateField(null=True, unique = True)
    endDate = models.DateField(null=True, unique = True)
    dueDate = models.DateField(null=True, unique = True)
    daysInCycle = models.IntegerField(default = 30)

    def __str__(self):
        return f"{self.fullName}"


# def date_to_billingcycle(date_to_check : date):

#     bill_cycles = BillingCycle.objects.all()

#     sel_bc_code = None
#     for bc in bill_cycles:

#         print(date(bc.endDate))

#         if (date(bc.endDate) >= date_to_check) & (date(bc.startDate) <= date_to_check):
#             sel_bc_code = bc.code
            

#     return sel_bc_code


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Income'),
        ('EX', 'Expense'),
    ]
    
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    billingCycle = models.CharField(max_length=50)#, default=date_to_billingcycle(date))
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_transaction_type_display()})"






    