from categories.models import Category


class DefaultCategoryFactory(object):

    def __init__(self):
        self.languages = ['en', 'es']
        self.categories = [['Car', 'Carro'],
                           ['House', 'Casa'],
                           ['Credit cards', 'Tarjetas de crédito'],
                           ['Electricity', 'Electricidad'],
                           ['Water', 'Agua'],
                           ['Rent', 'Alquiler'],
                           ['Insurance', 'Seguros'],]

    def create_defaults(self):
        default_categories = list()
        for category_list in self.categories:
            category = Category.objects.create(name=category_list[0],
                                               _current_language=self.languages[0],
                                               is_public=True)
            category.set_current_language(self.languages[1])
            category.name = category_list[1]
            category.save()
            default_categories.append(category)
        return default_categories
