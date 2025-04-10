import requests
from bs4 import BeautifulSoup
found = False

class CodeFinder:
    def __init__(self, url):
        self.url = self.fix_url(url)
        self.html_content = self.fetch_html()
        self.soup = BeautifulSoup(self.html_content, "html.parser") if self.html_content else None

    def fix_url(self, url):
        #if the URL doesnt itself contain //
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        return url

    def fetch_html(self):
        try:
            response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 403:
                return f"Error: Access forbidden (403) when trying to fetch"
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(" Error fetching URL: {e}")
            return None



    def search_script_tags(self, search_text):
        if not self.soup:
            return "Couldnt extract params from the website"

        script_tags = self.soup.find_all("script")

        for script in script_tags:
            if script.string and search_text.lower() in script.string.lower():
                return "The client has installed the code."

            if script.has_attr("src") and search_text.lower() in script["src"].lower():
                print("The client is using the code")
                return "The client is using the code"
                found = True

        # print(" '{search_text}' not found in <script> tags.")  # Debugging
        # return " '{search_text}' not found in <script> tags."
        #return "Couldn't extract from the Website."



    def search_style_tags(self, search_text):
        # to search the plugin
        if not self.soup:
            return " Couldnt find the plugin."

        style_tags = self.soup.find_all("style")
        for style in style_tags:
            if style.string and search_text.lower() in style.string.lower():
                return "The client is using the chat plugin"
                found = True

        

    def if_found():
        if found == False:
            return "URL Extraction Unsuccessfull"
        else:
            print("extraction succuessfull")
            return "extraction succuessfull"


    