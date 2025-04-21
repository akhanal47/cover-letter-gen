import requests
from bs4 import BeautifulSoup

class getWorkdayContent:
    # returns the html content of the LinkedIn page
    def _getWorkday_html(workday_url):
        try:
            response = requests.get(workday_url)
            return response.content
        except Exception as e:
            return f"Error fetching Workday content:{e}"

    @staticmethod
    def getWorkday(workday_url):
        workday_html = getWorkdayContent._getWorkday_html(workday_url)

        # if there's no error from the getWorkday_html
        if str(workday_html).startswith("Error"):
            return f"Error fetching Workday content:{workday_html}"
        
        # else parse
        try:
            html_soup = BeautifulSoup(workday_html, 'html.parser')
            workday_content = html_soup.find('article', class_='cms-content')
            try:
                workday_jd = workday_content.get_text().split("Benefits")[0]
                return workday_jd
            except:
                return workday_content.get_text()
        except:
            return f"Error fetching Workday content:{workday_html}"
        