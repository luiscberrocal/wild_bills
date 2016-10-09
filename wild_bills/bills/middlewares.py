from .utils import organization_manager


class AutoSelectOrganizationMiddleware(object):

    def process_request(self, request):
        if not request.user or not request.user.is_authenticated():
            return

        orga = organization_manager.get_selected_organization(request)
        if orga is not None:
            return

        user_orgas = organization_manager.get_user_organizations(request.user)
        if user_orgas.count():
            orga = user_orgas.first()
            organization_manager.set_selected_organization(request, orga)

class AutoSelectOrganizationMiddleware110(object):


    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self._process_request(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def _process_request(self, request):
        if not request.user or not request.user.is_authenticated():
            return

        orga = organization_manager.get_selected_organization(request)
        if orga is not None:
            return

        user_orgas = organization_manager.get_user_organizations(request.user)
        if user_orgas.count():
            orga = user_orgas.first()
            organization_manager.set_selected_organization(request, orga)

