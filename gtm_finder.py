import asyncio
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

gtm_search = "invitation.ashx"

async def capture_all_requests(url):
    # Ensure the URL starts with "http://" or "https://"
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to https:// if no protocol is provided

    print(f"Visiting URL: {url}")  # Log to confirm URL 

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        cdp_session = await context.new_cdp_session(page)
        await cdp_session.send("Network.enable")

        captured_requests = []
        gtm_found = False # Flag to check if GTM is found

        

        def handle_request_will_be_sent(params):
            nonlocal gtm_found  # Access the outer scope variable
            req_obj = params["request"]
            url_ = req_obj.get("url", "")
            post_data = req_obj.get("postData", "")

            parsed_url = urlparse(url_)
            query_params = parse_qs(parsed_url.query)

            captured_requests.append({
                "url": url_,
                "postData": post_data,
                "query_params": query_params
            })
            
            # print("The has installed the code through GTM")

        cdp_session.on("Network.requestWillBeSent", handle_request_will_be_sent)

        await page.goto(url)
        await page.wait_for_timeout(5000)
        await browser.close()

        print(f"Captured requests: {captured_requests}")
        return captured_requests
        


def gtm_search_parameter():
        #defining the search param for GTM
        gtm_search = "invitation.ashx"
        return gtm_search