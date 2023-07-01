
from cheapsharkapi import return_cheapest as rc
from cheapsharkapi import return_game as rg
from cheapsharkapi import set_alert as sa
from cheapsharkapi import manage_alerts as ma
from flask import Flask, request, render_template, session
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

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="rnicosia",
    password=SQLPASS,
    hostname="rnicosia.mysql.pythonanywhere-services.com",
    databasename="rnicosia$cheapgames",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    # user_input_data.append(request.form["contents"])


@app.route('/fun', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get question and model from form
        question = request.form.get('question')
        model = request.form.get('model')

        # Initialize the 'messages' session variable if it doesn't exist
        if 'messages' not in session:
            session['messages'] = [{
                "role": "system",
                "content": "You are a helpful assistant."
            }]

        # Add the new user message
        session['messages'].append({
            "role": "user",
            "content": question
        })

        # Make API request
        response = openai.ChatCompletion.create(
            model=model,
            messages=session['messages']
        )

        # Add the new assistant message
        session['messages'].append({
            "role": "assistant",
            "content": response['choices'][0]['message']['content']
        })

        # Get the answer
        answer = response['choices'][0]['message']['content']

        # Render the template with the answer
        return render_template('ask_gpt.html', answer=answer)
    else:
        return render_template('ask_gpt.html')


if __name__ == '__main__':
    app.run(debug=False)
