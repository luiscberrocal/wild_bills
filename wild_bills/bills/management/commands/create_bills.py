from django.core.management import BaseCommand

from ...models import Debt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?')
        # parser.add_argument('--true-false-arg',
        #                     action='store_true',
        #                     dest='true_or_false_arg',
        #                     default=None,
        #                     help='Useful info')
        # parser.add_argument('--variable',
        #                     action='store',
        #                     dest='variable_name',
        #                     default=None,
        #                     help='Useful info')
        # parser.add_argument('--appended-argument',
        #                     action='append',
        #                     dest='appended_arg',
        #                     default=None,
        #                     help='Useful info')

    def handle(self, *args, **options):
        debts = Debt.objects.filter(organization__owner__username=options['username'])
        count = 1
        for debt in debts:
            bills_created = debt.create_bills(1)
            for bill in bills_created:
                self.stdout.write('%d Created bills for %s %.2f %s' % (count, debt.payee, debt.amount,
                                                                    bill.due_date.strftime('%Y-%m-%d')))
                count += 1


