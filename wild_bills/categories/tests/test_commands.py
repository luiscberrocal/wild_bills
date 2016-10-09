from django.core.management import call_command
from django.test import TestCase

from ..models import Category


class CommandsTestCase(TestCase):

    def test_category_import_defaults(self):
        args = []
        opts = {'load_defaults': True}
        call_command('category_import', *args, **opts)
        categories = Category.objects.all()
        self.assertEquals(7, len(categories))
