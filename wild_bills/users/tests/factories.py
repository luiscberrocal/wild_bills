import factory
from faker import Factory as FakerFactory


__author__ = 'luiscberrocal'

faker = FakerFactory.create()

# class UserFactory(factory.django.DjangoModelFactory):
#     username = factory.Sequence(lambda n: 'user-{0}'.format(n))
#     email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
#     password = factory.PostGenerationMethodCall('set_password', 'password')
#
#     class Meta:
#         model = 'users.User'
#         django_get_or_create = ('username', )

class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )

    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    password = 'user1'
    country = 'PA'

    @factory.lazy_attribute
    def username(self):
        return '%s.%s' % (self.first_name.lower(), self.last_name.lower())

    @factory.lazy_attribute
    def email(self):
        return '%s@example.com' % self.username

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
