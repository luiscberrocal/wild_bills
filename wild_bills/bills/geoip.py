import socket
from django.conf import settings
import re
from urllib.request import urlopen, Request

__author__ = 'luiscberrocal'

class GeoIPFinder(object):

    def __init__(self):
        self.domain_re = re.compile('^(http|https):\/\/?([^\/]+)')
        self.domain = 'www.example.com' #self.domain_re.match(settings.SITE_URL).group(2)
        self.url_query_template = "http://api.wipmania.com/%s?%s"

    def get_country_code(self, ip_address):
        if ip_address is None:
            return None

        url =  self.url_query_template % (ip_address , self.domain)
        socket.setdefaulttimeout(5)
        headers = {'Typ':'django','Ver':'1.8.6','Connection':'Close'}
        try:
            req = Request(url, None, headers)
            with urlopen(req) as url_file:
                land = url_file.read()
            return str(land[:2], 'utf-8')
        except Exception:
            return None

geo_ip_finder = GeoIPFinder()