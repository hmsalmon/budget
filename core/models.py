from django.db import models

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
    billingCycle = models.CharField(max_length=50, default= "Dec25")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_transaction_type_display()})"

class BillingCycle(models.Model):

    code = models.CharField(max_length=5)
    fullName = models.CharField(max_length=14)
    displayName = models.CharField(max_length=24)
    startDate = models.DateField()
    endDate = models.DateField()
    dueDate = models.DateField()
    daysInCycle = models.IntegerField()

    def __str__(self):
        return f"{self.fullName}"




    