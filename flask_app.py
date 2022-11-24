import requests
from cheapsharkapi import return_cheapest as rc
from flask import Flask, render_template, redirect, request, url_for
import os

# https://apidocs.cheapshark.com/

SQLPASS = os.getenv("SQLPASS")
'''
CHEAPSHARK_API_DEALS = "https://www.cheapshark.com/api/1.0/deals"
CHEAPSHARK_API_STORES = "https://www.cheapshark.com/api/1.0/stores"
CHEAPSHARP_REDIRECT = "https://www.cheapshark.com/redirect?dealID="
store_response_init = requests.get(url=CHEAPSHARK_API_STORES)
store_response_init.raise_for_status()
store_response_init_json = store_response_init.json()
#deals_params = {
#    "sortBy": "Price",
#    "pageNumber": page_number,
#    "lowerPrice": lower_price,
#    "upperPrice": upper_price,
#}
cheapshark_response = requests.get(url=CHEAPSHARK_API_DEALS, params=deals_params)
cheapshark_response.raise_for_status()
cheapshark_response_json = cheapshark_response.json()
'''

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

#user_input_data = []
input_data = ''

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html")
    elif request.method == "POST":
        if request.form['get_games'] == "Free Games":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 0,
                "upperPrice": 0,
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games Under $10":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 0.01,
                "upperPrice": 10,
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $10 to $20":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 10,
                "upperPrice": 20,
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $20 to $30":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 20,
                "upperPrice": 30,
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $30 to $40":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 30,
                "upperPrice": 40,
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $40 to $50":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 40,
                "upperPrice": 49.99,
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games Over $50":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 50,
                "upperPrice": 50,
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif requests.form['game_title_button'] == "Search":
            input_data = request.form['game_title_text']
            deals_params = {
                "sortBy": "Price",
                "title": input_data
            }
            cheapshark_data = rc(deals_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
    #user_input_data.append(request.form["contents"])

@app.route('/wibble')
def wibble():
    return cheapshark_response_json
