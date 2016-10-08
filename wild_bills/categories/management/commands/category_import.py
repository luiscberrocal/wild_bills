from django.core.management import BaseCommand
from ...utils import DefaultCategoryFactory

class Command(BaseCommand):
    def add_arguments(self, parser):
        # parser.add_argument('optional-argument', nargs='?')
        parser.add_argument('--defaults',
                            action='store_true',
                            dest='load_defaults',
                            default=None,
                            help='Load default categories')
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
        if options['load_defaults']:

            category_factory = DefaultCategoryFactory()
            categories = category_factory.create_defaults()
            for category in categories:
                self.stdout.write('[+] Category %s' % category.name)
