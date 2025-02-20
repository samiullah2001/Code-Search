import requests
from bs4 import BeautifulSoup

codefound = False
class CodeFinder:
    def __init__(self, url):
        self.url = url
        self.html_content = self.fetch_html()
        self.soup = BeautifulSoup(self.html_content, "html.parser")
        #this line of code is used to extract/parse html code
        global codefound

    def fetch_html(self):
        "Fetch the HTML content of a webpage."
        response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        return response.text

    #the below code search for when the Blazeo code is directly added in the website.
    def search_script_tags(self, search_text):
        script_tags = self.soup.find_all("script")
        found = False

        for script in script_tags:
            if script.string and search_text in script.string:
                found = True
            if script.has_attr("src") and search_text in script["src"]:
              print("The company has added the direct code")

              found = True



    #the below code search for when the Blazeo plugin is added to the website.
    def search_style_tags(self, search_text):
        style_tags = self.soup.find_all("style")
        found = False

        for style in style_tags:
            if style.string and search_text in style.string:
                #print(" Found '{search_text}' in <style> tag")
                print("The company is using the plugin")
                found = True



# Example Usage
url = input("Enter URL:")
searching = CodeFinder(url)


search_text_script = "invitation.ashx"
search_text_style = "#apexchat_prechat_invitation_wrapper"

searching.search_script_tags(search_text_script)
searching.search_style_tags(search_text_style)