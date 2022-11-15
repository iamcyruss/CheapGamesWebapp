import requests
from cheapsharkapi import return_cheapest as rc
from flask import Flask, render_template

# https://apidocs.cheapshark.com/

CHEAPSHARK_API_DEALS = "https://www.cheapshark.com/api/1.0/deals"
CHEAPSHARK_API_STORES = "https://www.cheapshark.com/api/1.0/stores"
CHEAPSHARP_REDIRECT = "https://www.cheapshark.com/redirect?dealID="
store_response_init = requests.get(url=CHEAPSHARK_API_STORES)
store_response_init.raise_for_status()
store_response_init_json = store_response_init.json()
deals_params = {
    "sortBy": "Price"
}
cheapshark_response = requests.get(url=CHEAPSHARK_API_DEALS, params=deals_params)
cheapshark_response.raise_for_status()
cheapshark_response_json = cheapshark_response.json()
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("main_page.html")


@app.route('/wibble')
def wibble():
    return cheapshark_response_json
    #return rc(cheapshark_response_json=cheapshark_response_json, store_response_init_json=store_response_init_json)
    #return 'This is my pointless new page'
