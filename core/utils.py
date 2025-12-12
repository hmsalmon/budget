from datetime import date
from .models import BillingCycle


def date_to_billingcycle(date : date):

    bill_cycles = BillingCycle.objects.all()

    sel_bc_code = None
    for bc in bill_cycles:
        if bc.endDate >= date & bc.startDate <= date:
            sel_bc_code = bc.code
            

    return sel_bc_code

