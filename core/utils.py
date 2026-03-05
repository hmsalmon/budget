from datetime import date
from .models import BillingCycle, Transaction

# def create_transaction(date, description, amount):
#     cycle = BillingCycle.objects.get(
#         startDate__lte=date,
#         endDate__gte=date
#     )

#     return Transaction.objects.create(
#         billing_cycle=cycle,
#         description=description,
#         amount=amount
#     )

# def date_to_billingcycle(date_to_check : date):

#     bill_cycles = BillingCycle.objects.all()

#     sel_bc_code = None
#     for bc in bill_cycles:

#         print(date(bc.endDate))

#         if (date(bc.endDate) >= date_to_check) & (date(bc.startDate) <= date_to_check):
#             sel_bc_code = bc.code
            

#     return sel_bc_code