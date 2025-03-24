from flask import Flask, render_template, request, jsonify, json
from code_finder import CodeFinder
from  gtm_finder import capture_all_requests, gtm_search_parameter
from gtm_finder import gtm_search
from rocket_lazy import extract_urls_with_keyword


import asyncio
import nest_asyncio
nest_asyncio.apply()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        website_url = request.form.get("website_url")

        if not website_url:
            return render_template("index.html", script_result="Please enter a valid URL.")
        finder = CodeFinder(website_url)

        # #search parameters for direct code & the plugin
        search_text_script = "invitation" # for direct code
        search_text_style = "#apexchat_prechat_invitation_wrapper" #for plugin
        search_parameter = "invitation"

        script_result = finder.search_script_tags(search_text_script)
        style_result = finder.search_style_tags(search_text_style)
        # search_parameter_script = finder.search_script_tags(search_parameter)
        # search_parameter_style = finder.search_style_tags(search_parameter)
        

        print(f"Script result: {script_result}")   
        print(f"Style result: {style_result}")
        # print(f"Style result: {search_parameter_script}")
        # print(f"Style result: {search_parameter_style}")

    #code to handle GTM    

    # Run the asynchronous function for GTM
        loop = asyncio.get_event_loop()
        requests_data = loop.run_until_complete(capture_all_requests(website_url))
        print(f"Type of requests_data: {type(requests_data)}")
        # Filter the requests where 'search_param' is found in the query parameters
        gtm_search = gtm_search_parameter()
        
        
        gtm = "invitation.ashx"
        filtered_requests = []
        for req in requests_data:
            if gtm in req["url"]:
                filtered_requests.append({
                    "url": req["url"],
                    "query_params": req["query_params"],
                    "postData": req["postData"]
                })
                
        keyword = "invitation"
        rocket_results = extract_urls_with_keyword(website_url, keyword)
        
    #code for rocket lazy
    # results_rocket = []
    # if request.method == "POST":
    #     website_url = request.form.get("website_url")
    #     keyword = request.form.get("keyword", "invitation")

    #     if website_url:
    #         results_rocket = extract_urls_with_keyword(website_url, keyword)

        # extracted_data = []
        gtms = "invitation"

        # if request.method == "POST":
        #     website_url = request.form.get("website_url")
            
        if website_url:
            extracted_data = extract_urls_with_keyword(website_url, gtms)
        

        stored_data = [{"url": item["full_url"], "params": item["query_params"]} for item in extracted_data if isinstance(extracted_data, list)]
           

        return render_template("index.html", script_result=script_result, style_result=style_result, requests=filtered_requests, website_url=website_url, stored_data=stored_data, rocket_results=rocket_results) 
        # extracted_data=extracted_data, stored_data=stored_data
            

    return render_template("index.html", requests=[])  #to Show the input form on GET request

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
