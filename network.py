import asyncio
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

async def network_calls(url):
    output = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        async def handle_request_or_response(request=None, response=None):
            if request:
                url = request.url.lower()
                if request.method == "GET" and "invitation" in url and "company" in url:
                    parsed_url = urlparse(request.url)
                    query_params = parse_qs(parsed_url.query)
                    company_value = query_params.get("company")
                    if company_value:
                        msg = f"\nFound 'invitation' and 'company' in URL: {request.url} \n"
                        company_msg = f"\nExtracted company value: {company_value[0]} \n"
                        output.extend([msg, company_msg])

            elif response:
                try:
                    text = await response.text()
                    if "invitation" in text.lower() and "company" in text.lower():
                        
                        msg = f"\nFound 'invit' in response from: {response.url} \n"

                        output.append(msg)
                except Exception as e:
                    pass 

        page.on("request", lambda req: asyncio.create_task(handle_request_or_response(request=req)))
        page.on("response", lambda res: asyncio.create_task(handle_request_or_response(response=res)))


        try:
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            await page.keyboard.press("Tab")
            await page.wait_for_timeout(8000)
        except Exception as e:
            output.append("Error: {str(e)}")

        await browser.close()

    return output
