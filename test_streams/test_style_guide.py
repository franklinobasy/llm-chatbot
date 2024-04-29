'''
The api streams input text as a text that conforms to CCL style guide
'''


import requests

# Replace with the appropriate URL where your FastAPI server is running
host="54.174.77.47"
# host ="localhost:8000"
api_url = f"http://{host}/api/v1/style_engine"

text = '''
Summer in the small American town brought a symphony of sounds that danced
 through the air like a nostalgic melody. Childrens laughter echoed from the 
 sun-baked playgrounds as they chased each other around, their energy unabated 
 by the sweltering heat. Family barbecues sizzled in backyards, with the smoky 
 aroma of grilled burgers and sweet corn wafting over picket fences, tempting 
 neighbors to gather and indulge. Teenagers cruised down Main Street in their 
 freshly washed cars, windows down, with the latest hits spilling out onto the 
 sidewalk where folks sipped iced teas and lemonades, waving to passersby. 
 It was the quintessential summer setting, one that celebrated community, 
 simplicity, and the enduring American spirit of making the most of these long, lazy days.
'''
# Replace with your actual prompt
data = {
    "text": text,
}

try:
    response = requests.post(
        api_url,
        params=data,
        stream=True,
        headers={"accept": "application/json"},
    )

    if response.status_code == 200:
        for chunk in response.iter_content():
            if chunk:
                try:
                    print(str(chunk, encoding="utf-8"), end="")
                except Exception as e:
                    pass
    else:
        print(f"Error: {response.status_code}\n{response.text}")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
