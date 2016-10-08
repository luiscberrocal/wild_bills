from django.test import TestCase

from ..geoip import geo_ip_finder


class TestGeoIPFinder(TestCase):

    def test_get_country_code(self):
        us_ip = '24.233.171.82'
        country_code = geo_ip_finder.get_country_code(us_ip)
        self.assertEqual('US', country_code)
