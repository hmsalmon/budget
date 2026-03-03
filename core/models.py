from django.db import models
from datetime import date

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
    billing_cycle = models.ForeignKey(
        BillingCycle,
        on_delete=models.PROTECT,
        related_name="transactions",
        null=True,
        blank=True
        )
    
    #billingCycle = models.CharField(max_length=50)#, default=date_to_billingcycle(date))
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.billing_cycle_id:
            self.billing_cycle = BillingCycle.objects.filter(
                start_date__lte=self.date,
                end_date__gte=self.date
            ).get()  # use get() if cycles never overlap

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_transaction_type_display()})"






    