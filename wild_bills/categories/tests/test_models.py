from django.test import TestCase
from django.utils import translation
from parler.utils import get_active_language_choices
from parler.utils.conf import LanguagesSetting

from .factories import CategoryFactory, category_factory
from ..models import Category


class TestCategory(TestCase):


    def test_create(self):
        category = Category.objects.create(name='Car')
        self.assertEqual(1, Category.objects.count())
        self.assertEqual('Car', category.name)
        self.assertEqual('en', category.get_current_language())

    def test_create_force_language_en(self):
        category = Category.objects.create(name='Car', _current_language='en')
        self.assertEqual(1, Category.objects.count())
        self.assertEqual('Car', category.name)
        self.assertEqual('en', category.get_current_language())

    def test_language_codes(self):
        codes = ['en', 'es']
        active_codes = get_active_language_choices()
        for code in codes:
            self.assertTrue(code in active_codes)


    def test_create_i18n(self):
        category = Category.objects.create(name='Car')
        self.assertEqual(1, Category.objects.count())
        self.assertEqual('Car', category.name)
        self.assertEqual('en', category.get_current_language())
        self.assertEqual('/en/categories/car/', category.get_absolute_url())

        translation.activate('es')
        category.set_current_language('es')
        self.assertEqual('es', category.get_current_language())
        category.name = 'Carro'
        category.save()
        self.assertEqual('/es/categories/carro/', category.get_absolute_url())

        self.assertEqual('Carro', category.name)
        tr_category = Category.objects.language('es').get(pk=category.pk)
        self.assertEqual('Carro', tr_category.name)
        tr_category = Category.objects.language('en').get(pk=category.pk)
        self.assertEqual('Car', tr_category.name)

    def test_create_defaults(self):
        categories = category_factory.create_defaults()
        self.assertEqual(7, len(categories))

        category = Category.objects.filter(translations__slug='electricidad')[0]

        self.assertEqual('Electricity', category.name)
        category.set_current_language('es')
        self.assertEqual('Electricidad', category.name)

        category = Category.objects.translated('es', slug='carro')[0]
        self.assertEqual('Car', category.name)


