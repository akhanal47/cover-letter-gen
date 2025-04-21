import requests
from bs4 import BeautifulSoup
import json

class getIcmsContent:

    def _stripHTMLTags(json_string):
        soup = BeautifulSoup(json_string, 'html.parser')
        clean_text = soup.get_text(separator=' ', strip=True)
        return clean_text

    def _getIcms_html(icms_url):
        try:
            response = requests.get(icms_url)
            return response.content
        except Exception as e:
            return f"Error fetching ICMS content:{e}"
        
    @staticmethod
    def getIcms(icms_url):
        icms_html = getIcmsContent._getIcms_html(icms_url)

        # if there's no error from the getWorkday_html
        if str(icms_html).startswith("Error"):
            return f"Error fetching ICMS content:{icms_html}"
        
        try:
            # else parse, join and return
            html_soup = BeautifulSoup(icms_html, 'html.parser')
            icms_json_raw = html_soup.find('script', {'type': 'application/ld+json'})    # this returns a json schema
            icms_json_content = json.loads(icms_json_raw.string)

            # get the content from the json schema
            jd_title = getIcmsContent._stripHTMLTags(icms_json_content.get('title'))
            jd_description = getIcmsContent._stripHTMLTags(icms_json_content.get('description'))
            jd_qualifications = getIcmsContent._stripHTMLTags(icms_json_content.get('qualifications'))
            jd_responsibilities = getIcmsContent._stripHTMLTags(icms_json_content.get('responsibilities'))

            # return the joined content if the conntent has something on it else error
            full_jd = " ".join([jd_title, jd_description, jd_qualifications, jd_responsibilities])
            if full_jd.strip(" ") == "":
                return "Error fetching ICMS content: No content found"
            return " ".join([jd_title, jd_description, jd_qualifications, jd_responsibilities])
        
        except:
            return f"Error fetching ICMS content:{icms_html}"