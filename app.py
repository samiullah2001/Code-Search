from flask import Flask, render_template, request
from code_finder import CodeFinder
from  gtm_finder import capture_all_requests

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

        # #search parameters
        search_text_script = "invitation.ashx" # for direct code
        search_text_style = "#apexchat_prechat_invitation_wrapper" #for plugin

        script_result = finder.search_script_tags(search_text_script)
        style_result = finder.search_style_tags(search_text_style)

        print(f"Script result: {script_result}")   
        print(f"Style result: {style_result}")   

    # Run the asynchronous capture function
        loop = asyncio.get_event_loop()
        requests_data = loop.run_until_complete(capture_all_requests(website_url))
        # Filter the requests where 'search_param' is found in the query parameters
        filtered_requests = []
        for req in requests_data:
            if search_text_script in req["url"]:
                filtered_requests.append({
                    "url": req["url"],
                    "query_params": req["query_params"],
                    "postData": req["postData"]
                })

        return render_template("index.html", script_result=script_result, style_result=style_result, 
                               requests=filtered_requests, website_url=website_url)
        
        

    return render_template("index.html")  #to Show the input form on GET request



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
