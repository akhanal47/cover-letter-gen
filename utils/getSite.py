import requests
from bs4 import BeautifulSoup
import regex

class getSite:
    @staticmethod
    def getDomain(url):
        pattern = r'^(?P<protocol>https?://)?(?P<domain>[^:/?#]+)(?::(?P<port>\d+))?(?P<path>[^?#]*)\??(?P<query>[^#]*)#?(?P<fragment>.*)$'
        match = regex.match(pattern, url)
        if match:
            domain = match.group('domain') or ''
            return domain
        return "Error Getting Domain"
