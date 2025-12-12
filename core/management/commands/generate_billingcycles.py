from django.core.management.base import BaseCommand
from datetime import date
from core.models import BillingCycle
import calendar

class Command(BaseCommand):
    help = "Generate New Billing Cycles"

    def add_arguments(self, parser):
        parser.add_argument("year", type=int)

        return super().add_arguments(parser)

    def handle(self, *args, **options):

        year_to_generate = options["year"]
  
        monthList= {1:'January',
                    2:"February",
                    3:"March",
                    4:"April",
                    5:"May",
                    6:"June",
                    7:"July",
                    8:"August",
                    9:"September",
                    10:"October",
                    11:"November",
                    12:"December"}
        
        endDay= {1:14,
                2:11,
                3:14,
                4:13,
                5:14,
                6:13,
                7:14,
                8:14,
                9:13,
                10:14,
                11:13,
                12:14}
        
        created_count = 0
        for month in list(range(1,13)):
            
            date_test = date(year_to_generate,month,1)

            yr = date_test.year
            mon = date_test.month
            day = date_test.day

            statement_mon = mon 
            statement_yr = yr

            if (day > endDay[mon]):
                statement_mon += 1        
                if (mon == 12):
                    statement_yr += 1
                    statement_mon = 1

            prev_state_mon = ((statement_mon - 1 - 1) % 12) + 1
            prev_state_year = statement_yr - int(prev_state_mon == 12)

            startDay = endDay[statement_mon] - calendar.monthrange(statement_yr,statement_mon)[1] + calendar.monthrange(prev_state_year,prev_state_mon)[1] + 1
        
            # self.stdout.write(self.style.SUCCESS(f"statement_mon: {statement_mon}"))
            # self.stdout.write(self.style.SUCCESS(f"statement_yr: {statement_yr}"))
            # self.stdout.write(self.style.SUCCESS(f"prev_state_mon: {prev_state_mon}"))
            # self.stdout.write(self.style.SUCCESS(f"prev_state_year: {prev_state_year}"))
            # self.stdout.write(self.style.SUCCESS(f"startDay: {startDay}"))

            full = f"{monthList[statement_mon]} {statement_yr}"
            display = f"{full} Statement"
            code = f"{monthList[statement_mon][:3]}{str(statement_yr)[2:]}"

            #self.stdout.write(self.style.ERROR(f"full: {full}")) #debug only
            #self.stdout.write(self.style.ERROR(f"code: {code}")) #debug only

            _, created = BillingCycle.objects.get_or_create(startDate=date(prev_state_year,prev_state_mon,startDay),
                                                              endDate=date(statement_yr,statement_mon,endDay[statement_mon]),
                                                              code=code,
                                                              fullName=full,
                                                              displayName=display,
                                                              daysInCycle=calendar.monthrange(statement_yr,statement_mon)[1])

            if created:
                created_count += 1
            

        self.stdout.write(self.style.SUCCESS(f"{created_count} Billing Cycles Created"))