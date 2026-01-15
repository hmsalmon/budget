from datetime import date
from .models import BillingCycle, Transaction

def create_transaction(date, description, amount):
    cycle = BillingCycle.objects.get(
        start_date__lte=date,
        end_date__gte=date
    )

    return Transaction.objects.create(
        billing_cycle=cycle,
        description=description,
        amount=amount
    )

