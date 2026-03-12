from datetime import date, timedelta
from core.models import Date
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Generating Dates"

    def handle(self, *args, **options):

        start = date(2036,5,1)
        end = date(2036,5,1)

        dayNames = {
            0:"Monday",
            1:"Tuesday",
            2:"Wednesday",
            3:"Thursday",
            4:"Friday",
            5:"Saturday",
            6:"Sunday"
        }

        monthNames = {
            1:"January",
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
            12:"December"
        }

        current = start

        numCreated = 0

        while current <= end:

            print(current)
            print(current.year)
            print(current.month)
            print(current.day)
            print(current.isocalendar()[1])
            print(monthNames[current.month])
            print(dayNames[current.weekday()])
            print(current.weekday() >= 5)

            # _, created = Date.objects.get_or_create(
            #     date=current,
            #     year=current.year,
            #     month=current.month,
            #     day=current.day,
            #     week=current.isocalendar()[1],
            #     monthName=current.month,
            #     weekdayName=current.weekday(),
            #     isWeekend=current.weekday() >= 5
            # )

            current += timedelta(days=1)

            if True:
                numCreated += 1
        

        self.stdout.write(self.style.SUCCESS(f"{numCreated} Dates Created"))