from ...users.tests.factories import UserFactory
from ..models import Category
from faker import Factory as FakerFactory
from ..utils import DefaultCategoryFactory

faker = FakerFactory.create()

class CategoryFactory(DefaultCategoryFactory):


    def create(self, name=None, owner=None, is_public=False, language=None):
        if not name:
            name = faker.word()
        if not owner and is_public == False:
            owner = UserFactory.create()
        if not language:
            language = self.languages[0]
        category = Category.objects.create(name=name, owner=owner, is_public=is_public,
                                           _current_language=language)
        return category

category_factory = CategoryFactory()


