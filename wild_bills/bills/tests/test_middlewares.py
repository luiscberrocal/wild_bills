from unittest.mock import Mock

from django.test import TestCase

from ..models import Organization
from ..utils import OrganizationManager
from .factories import OrganizationFactory
from ..middlewares import AutoSelectOrganizationMiddleware


class TestAutoSelectOrganizationMiddleware(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory.create()
        self.middleware = AutoSelectOrganizationMiddleware()
        self.request = Mock()
        self.request.session = {}
        self.request.user = self.organization.owner
        #self.request.user.is_authenticated = True


    def test_auto_select(self):

        key = OrganizationManager.selected_organization_key
        #self.request.session = {key: organization.pk}
        self.assertIsNone(self.middleware.process_request(self.request))
        self.assertEqual(self.request.session[key], self.organization.pk)

    def test_auto_select_several_orgs(self):
        first_org = OrganizationFactory.create()
        organization = OrganizationFactory.create(owner=first_org.owner)
        request = Mock()
        request.session = {}
        request.user = first_org.owner
        key = OrganizationManager.selected_organization_key

        self.assertEqual(3, Organization.objects.count())
        self.assertIsNone(self.middleware.process_request(request))
        self.assertEqual(request.session[key], first_org.pk)

