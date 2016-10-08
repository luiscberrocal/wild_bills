from django import forms
from parler.forms import TranslatableModelForm

from .models import Category


class CategoryForm(TranslatableModelForm):

    class Meta:
        model = Category
        fields = ['name', 'is_public', ]