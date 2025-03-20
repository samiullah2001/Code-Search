import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def extract_urls_with_keyword(url, keyword):
    try:
        # Fetch website HTML
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all script tags with type="rocketlazyloadscript"
        lazy_scripts = soup.find_all("script", {"type": "rocketlazyloadscript"})

        # Extract URLs that contain the keyword
        matching_urls = []

        for script in lazy_scripts:
            data_src = script.get("data-rocket-src", "")
            if data_src and keyword in data_src:  # **Check if keyword exists in URL**
                parsed_url = urlparse(data_src)
                query_params = parse_qs(parsed_url.query)

                matching_urls.append({
                    "full_url": data_src,
                    "query_params": query_params
                })

        return matching_urls if matching_urls else f"No URLs found containing '{keyword}'."

    except requests.RequestException as e:
        return f"Error fetching page: {e}"