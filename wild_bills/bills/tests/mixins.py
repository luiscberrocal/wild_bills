from django.utils import translation

from .factories import WildBillsProfileFactory


class UserSetupMixin(object):

    def setUp(self):
        translation.activate('en')

        self.username = 'obiwan'
        self.password = 'password'
        self.profile = WildBillsProfileFactory.create(username=self.username,
                                                      password=self.password,
                                                      email='obiwan@jedi.org',
                                                      first_name='Obiwan',
                                                      last_name='Kenobi',)
        self.windu_profile = WildBillsProfileFactory.create(username='macewindu',
                                                      password='password',
                                                      email='mace@jedi.org',
                                                      first_name='Mace',
                                                      last_name='Windu',)
        self.profile_dict = {'username': 'spiderman',
                             'last_name': 'Parker',
                             'first_name': 'Peter',
                             'email': 'pparker@gmail.com',
                             'country': 'US',
                             'password1': 'kilo',
                             'password2': 'kilo'}