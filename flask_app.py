import requests
from cheapsharkapi import return_cheapest as rc
from cheapsharkapi import return_game as rg
from cheapsharkapi import set_alert as sa
from cheapsharkapi import manage_alerts as ma
from flask import Flask, render_template, redirect, request, url_for
import os
import openai

OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY
# https://apidocs.cheapshark.com/

SQLPASS = os.getenv("SQLPASS")
CHEAPSHARK_API_DEALS = "https://www.cheapshark.com/api/1.0/deals"
CHEAPSHARK_API_STORES = "https://www.cheapshark.com/api/1.0/stores"
CHEAPSHARP_REDIRECT = "https://www.cheapshark.com/redirect?dealID="
CHEAPSHARK_API_ALERT = "https://www.cheapshark.com/api/1.0/alerts"
'''
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
app.config["DEBUG"] = False

"""
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="rnicosia",
    password=SQLPASS,
    hostname="rnicosia.mysql.pythonanywhere-services.com",
    databasename="rnicosia$cheapgames",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
"""

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
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games Under $10":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 0.01,
                "upperPrice": 10,
            }
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $10 to $20":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 10,
                "upperPrice": 20,
            }
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $20 to $30":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 20,
                "upperPrice": 30,
            }
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $30 to $40":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 30,
                "upperPrice": 40,
            }
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games $40 to $50":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 40,
                "upperPrice": 49.99,
            }
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Games Over $50":
            deals_params = {
                "sortBy": "Price",
                "pageNumber": 0,
                "lowerPrice": 50,
                "upperPrice": 50,
            }
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Search":
            input_data = request.form['game_title_text']
            deals_params = {
                "sortBy": "Price",
                "title": input_data
            }
            cheapshark_data = rg(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Set Alert":
            price = request.form['price']
            email = request.form['email']
            gameid = request.form['gameid']
            alert_params = {
                "action": "set",
                "price": price,
                "email": email,
                "gameID": gameid
            }
            cheapshark_data = sa(CHEAPSHARK_API_ALERT, alert_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Delete Alert":
            price = request.form['price']
            email = request.form['email']
            gameid = request.form['gameid']
            alert_params = {
                "action": "delete",
                "price": price,
                "email": email,
                "gameID": gameid
            }
            cheapshark_data = sa(CHEAPSHARK_API_ALERT, alert_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Manage Alerts":
            email = request.form['manageemail']
            alert_params = {
                "action": "manage",
                "email": email
            }
            cheapshark_data = ma(CHEAPSHARK_API_ALERT, alert_params)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
        elif request.form['get_games'] == "Metacritic 90+ Games":
            deals_params = {
                "sortBy": "Price",
                "metacritic": 90
            }
            cheapshark_data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
            return render_template("main_page.html", cheapshark_data=cheapshark_data)
    #user_input_data.append(request.form["contents"])


@app.route('/fun')
def home():
    return render_template('ask_gpt.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Get question and model from form
    question = request.form.get('question')
    model = request.form.get('model')

    # Make API request
    response = openai.Completion.create(
        engine=model,
        prompt=question,
        max_tokens=100
    )

    # Get the answer
    answer = response.choices[0].text.strip()

    # Render the template with the answer
    return render_template('ask_gpt.html', answer=answer)

"""
if __name__ == '__main__':
    app.run(debug=False)
"""
