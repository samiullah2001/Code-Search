import requests
from bs4 import BeautifulSoup

class CodeFinder:
    def __init__(self, url):
        self.url = self.fix_url(url)
        self.html_content = self.fetch_html()
        self.soup = BeautifulSoup(self.html_content, "html.parser") if self.html_content else None

    def fix_url(self, url):
        """Ensure URL has the correct format."""
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        return url

    def fetch_html(self):
        """Fetch the HTML content of a webpage."""
        try:
            response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            print(f"✅ Successfully fetched HTML from: {self.url}")  # Debugging
            print(response.text[:500])  # Print first 500 characters
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching URL: {e}")  # Debugging
            return None



    def search_script_tags(self, search_text):
        """Search for a keyword inside <script> tags."""
        if not self.soup:
            print("❌ Error: No HTML content to parse.")
            return "❌ Error: Could not fetch HTML content."

        script_tags = self.soup.find_all("script")
        print(f"🔍 Found {len(script_tags)} script tags.")  # Debugging

        for script in script_tags:
            if script.string and search_text.lower() in script.string.lower():
                print(f"✅ Found '{search_text}' in inline script.")
                return f"✅ Found '{search_text}' in inline script."

            if script.has_attr("src") and search_text.lower() in script["src"].lower():
                print(f"✅ Found '{search_text}' in external script: {script['src']}")
                return f"✅ Found '{search_text}' in external script: {script['src']}"

        print(f"❌ '{search_text}' not found in <script> tags.")  # Debugging
        return f"❌ '{search_text}' not found in <script> tags."



    def search_style_tags(self, search_text):
        """Search for a keyword inside <style> tags."""
        if not self.soup:
            print("❌ Error: No HTML content to parse.")
            return "❌ Error: Could not fetch HTML content."

        style_tags = self.soup.find_all("style")
        print(f"🔍 Found {len(style_tags)} style tags.")  # Debugging

        for style in style_tags:
            if style.string and search_text.lower() in style.string.lower():
                print(f"✅ Found '{search_text}' in <style> tag.")
                return f"✅ Found '{search_text}' in <style> tag."

        print(f"❌ '{search_text}' not found in <style> tags.")  # Debugging
        return f"❌ '{search_text}' not found in <style> tags."

