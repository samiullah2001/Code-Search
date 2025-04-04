from flask import Flask, render_template, request
from code_finder import CodeFinder
from gtm_finder import capture_all_requests, gtm_search_parameter
from rocket_lazy import extract_urls_with_keyword
from network import network_calls

import asyncio
import nest_asyncio
nest_asyncio.apply()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        website_url = request.form.get("website_url")
        toggle_state = request.form.get("toggle") 

        if not website_url:
            return render_template("index.html", script_result="Please enter a valid URL.")

        # Common logic
        finder = CodeFinder(website_url)
        search_text_script = "invitation"
        search_text_style = "#apexchat_prechat_invitation_wrapper"
        script_result = finder.search_script_tags(search_text_script)
        style_result = finder.search_style_tags(search_text_style)

        print(f"Script result: {script_result}")   
        print(f"Style result: {style_result}")
        

        # Rocket Lazy
        keyword = "invitation"
        extracted_data = extract_urls_with_keyword(website_url, keyword)
        stored_data = [{"url": item["full_url"], "params": item["query_params"]} for item in extracted_data if isinstance(extracted_data, dict) or isinstance(item, dict)]

        # GTM Requests
        loop = asyncio.get_event_loop()
        requests_data = loop.run_until_complete(capture_all_requests(website_url))
        filtered_requests = [req for req in requests_data if keyword in req.get("url", "")]

        #network code
        network_result = asyncio.run(network_calls(website_url))

        # Handle toggle
        CodeFinderResult = script_result or style_result or filtered_requests or stored_data
        # GTM_RocketResult = filtered_requests or stored_data
        
        resultB = None
        if toggle_state == "B":
            resultB = CodeFinderResult
        else:
            resultB = network_result

        return render_template("index.html",
                               website_url=website_url,
                               network_result=network_result,
                               resultB=resultB)
        # original return
        # return render_template("index.html",
        #                        website_url=website_url,
        #                        script_result=script_result,
        #                        style_result=style_result,
        #                        requests=filtered_requests,
        #                        stored_data=stored_data,
        #                        network_result=network_result,
        #                        resultB=resultB)

    return render_template("index.html", requests=[])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


