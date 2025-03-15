import asyncio
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

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

        def handle_request_will_be_sent(params):
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
            print(f"Captured request: {url_}")  # Log captured requests

        cdp_session.on("Network.requestWillBeSent", handle_request_will_be_sent)

        await page.goto(url)
        await page.wait_for_timeout(5000)
        await browser.close()

        print(f"Captured requests: {captured_requests}")  # Log the final requests
        return captured_requests
