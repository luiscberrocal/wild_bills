from autoslug import AutoSlugField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from parler.fields import TranslatedField
from parler.models import TranslatableModel, TranslatedFields, TranslatedFieldsModel
from parler.utils.context import switch_language


# class AbstractCategory(TranslatableModel):
#     name = TranslatedField(any_language=True)
#     slug = TranslatedField()
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL,
#                               related_name="owned_categories",
#                               verbose_name=_('Owner'),
#                               null=True, blank=True)
#
#     is_public = models.BooleanField(default=False)
#
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.safe_translation_getter('name', any_language=True)
#
#     def get_absolute_url(self):
#         with switch_language(self):
#             return reverse('categories:category-detail', args=[self.slug])
#
#
# class AbstractCategoryTranslation(TranslatedFieldsModel):
#     """
#     The translated fields of the category.
#     By using this model instead of the ``parler.models.TranslatedFields(..)`` construct,
#     the translatable fields can be defined in an abstract model.
#     """
#     name = models.CharField(_('Name'), max_length=200)
#     slug = AutoSlugField(populate_from='name')
#     master = None #models.ForeignKey(Category, related_name='translations')
#
#     class Meta:
#         abstract = True
#         # verbose_name = _("Category Translation")
#         # verbose_name_plural = _("Category Translations")
#         unique_together = (
#             ('language_code', 'slug',),
#         )


class Category(TranslatableModel):

    translations = TranslatedFields(
        name = models.CharField(_("Name"), max_length=200),
        slug = AutoSlugField(populate_from='name')
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="owned_categories",
                              verbose_name=_('Owner'),
                              null=True, blank=True)

    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    def get_absolute_url(self):
        with switch_language(self):
            return reverse('categories:category-detail', args=[self.slug])

#
# class CategoryTranslation(AbstractCategoryTranslation):
#     """
#     The translated fields of the category.
#     By using this model instead of the ``parler.models.TranslatedFields(..)`` construct,
#     the translatable fields can be defined in an abstract model.
#     """
#     master = models.ForeignKey(Category, related_name='translations')
#
#     class Meta:
#         verbose_name = _("Category Translation")
#         verbose_name_plural = _("Category Translations")
