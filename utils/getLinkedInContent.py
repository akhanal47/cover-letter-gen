import requests
from bs4 import BeautifulSoup

class getLinkedInContent:
    @staticmethod
    # returns the html content of the LinkedIn page
    def _getLinkedIn_html(linkedin_url):
        try:
            response = requests.get(linkedin_url)
            htmlsoup = BeautifulSoup(response.content, 'html.parser')
            return htmlsoup
        except Exception as e:
            return f"Error fetching LinkedIn content:{e}"

    def getLinkedIn(linkedin_url):
        linkedin_html = getLinkedInContent._getLinkedIn_html(linkedin_url)
        # currently, there is now way to get the job description from LinkedIn without logging in, so always return an error
        return "Error fetching LinkedIn Job Description"
        #! Future Work
        # TODO: In the future, add logic to parse and return the description text if access is possible