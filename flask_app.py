import requests
from cheapsharkapi import return_cheapest as rc
from flask import Flask, render_template, redirect, request, url_for
import os

# https://apidocs.cheapshark.com/

SQLPASS = os.getenv("SQLPASS")
page_number = 10
lower_price = 0
upper_price = 50
CHEAPSHARK_API_DEALS = "https://www.cheapshark.com/api/1.0/deals"
CHEAPSHARK_API_STORES = "https://www.cheapshark.com/api/1.0/stores"
CHEAPSHARP_REDIRECT = "https://www.cheapshark.com/redirect?dealID="
store_response_init = requests.get(url=CHEAPSHARK_API_STORES)
store_response_init.raise_for_status()
store_response_init_json = store_response_init.json()
deals_params = {
    "sortBy": "Price",
    "pageNumber": page_number,
    "lowerPrice": lower_price,
    "upperPrice": upper_price,
}
cheapshark_response = requests.get(url=CHEAPSHARK_API_DEALS, params=deals_params)
cheapshark_response.raise_for_status()
cheapshark_response_json = cheapshark_response.json()

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="rnicosia",
    password=SQLPASS,
    hostname="rnicosia.mysql.pythonanywhere-services.com",
    databasename="rnicosia$cheapgames",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

data = rc(cheapshark_response_json, store_response_init_json)

user_input_data = []

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", cheapshark_data=data,
                               user_input_data=user_input_data,)

    user_input_data.append(request.form["contents"])
    return redirect(url_for('index'))

@app.route('/wibble')
def wibble():
    return cheapshark_response_json
