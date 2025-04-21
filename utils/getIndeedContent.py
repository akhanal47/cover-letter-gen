import requests
from bs4 import BeautifulSoup

class getLinkedInContent:
    @staticmethod
    # returns the html content of the LinkedIn page
    def _getIndeed_html(indeed_url):
        try:
            response = requests.get(indeed_url)
            htmlsoup = BeautifulSoup(response.content, 'html.parser')
            return htmlsoup
        except Exception as e:
            return f"Error fetching Indeed content:{e}"

    def getIndeed(indeed_url):
        indeed_html = getLinkedInContent._getIndeed_html(indeed_url)
        # currently, there is now way to get the job description from Indeed without logging in, so always return an error
        return "Error fetching Indeed Job Description"
        #! Future Work
        # TODO: In the future, add logic to parse and return the description text if access is possible