from cheapsharkapi import return_cheapest as rc
from cheapsharkapi import return_game as rg
from cheapsharkapi import set_alert as sa
from cheapsharkapi import manage_alerts as ma
from flask import Flask, request, render_template, session, current_app
import os
import openai
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from sqlalchemy.exc import OperationalError
from werkzeug.utils import secure_filename
import uuid
from dotenv import load_dotenv

load_dotenv(override=True)
print("🔑  DATABASE_URL→", os.getenv("DATABASE_URL"))

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

# CheapShark API endpoints
SQLPASS = os.getenv("SQLPASS")
CHEAPSHARK_API_DEALS  = "https://www.cheapshark.com/api/1.0/deals"
CHEAPSHARK_API_STORES = "https://www.cheapshark.com/api/1.0/stores"
CHEAPSHARP_REDIRECT   = "https://www.cheapshark.com/redirect?dealID="
CHEAPSHARK_API_ALERT  = "https://www.cheapshark.com/api/1.0/alerts"

# Neon Postgres credentials (via .env)
PGUSER     = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGHOST     = os.getenv("PGHOST")
PGPORT     = os.getenv("PGPORT", "5432")
PGDATABASE = os.getenv("PGDATABASE")

db = SQLAlchemy()
app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"]        = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_RECYCLE"]        = 280
app.config["SQLALCHEMY_POOL_SIZE"]           = 5
app.config["SQLALCHEMY_MAX_OVERFLOW"]        = 10

# Uploads configuration
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)

input_data = ''

class Conversation(db.Model):
    id       = db.Column(db.String(256), primary_key=True)
    messages = db.Column(db.Text)  # JSON list of {role, content}

def allowed_file(filename: str) -> bool:
    """Return True if the file extension is allowed."""
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def format_answer(answer: str) -> str:
    """Wrap code blocks in <pre><code> for HTML display."""
    parts = answer.split("```")
    out = []
    is_code = False
    for part in parts:
        if is_code:
            out.append(f"<pre><code>{part}</code></pre>")
        else:
            out.append(part)
        is_code = not is_code
    return "".join(out)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("main_page.html")

    choice = request.form.get('get_games')
    if choice == "Free Games":
        deals_params = {"sortBy": "Price", "pageNumber": 0, "lowerPrice": 0, "upperPrice": 0}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Games Under $10":
        deals_params = {"sortBy": "Price", "pageNumber": 0, "lowerPrice": 0.01, "upperPrice": 10}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Games $10 to $20":
        deals_params = {"sortBy": "Price", "pageNumber": 0, "lowerPrice": 10, "upperPrice": 20}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Games $20 to $30":
        deals_params = {"sortBy": "Price", "pageNumber": 0, "lowerPrice": 20, "upperPrice": 30}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Games $30 to $40":
        deals_params = {"sortBy": "Price", "pageNumber": 0, "lowerPrice": 30, "upperPrice": 40}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Games $40 to $50":
        deals_params = {"sortBy": "Price", "pageNumber": 0, "lowerPrice": 40, "upperPrice": 49.99}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Games Over $50":
        deals_params = {"sortBy": "Price", "pageNumber": 0, "lowerPrice": 50, "upperPrice": 50}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Search":
        title = request.form.get('game_title_text', '')
        deals_params = {"sortBy": "Price", "title": title}
        data = rg(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    elif choice == "Set Alert":
        alert_params = {
            "action": "set",
            "price": request.form.get('price'),
            "email": request.form.get('email'),
            "gameID": request.form.get('gameid')
        }
        data = sa(CHEAPSHARK_API_ALERT, alert_params)
    elif choice == "Delete Alert":
        alert_params = {
            "action": "delete",
            "price": request.form.get('price'),
            "email": request.form.get('email'),
            "gameID": request.form.get('gameid')
        }
        data = sa(CHEAPSHARK_API_ALERT, alert_params)
    elif choice == "Manage Alerts":
        alert_params = {"action": "manage", "email": request.form.get('manageemail')}
        data = ma(CHEAPSHARK_API_ALERT, alert_params)
    elif choice == "Metacritic 90+ Games":
        deals_params = {"sortBy": "Price", "metacritic": 90}
        data = rc(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT)
    else:
        data = None

    return render_template("main_page.html", cheapshark_data=data)


@app.route('/fun', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            # 1) gather and validate inputs
            question        = request.form.get("question", "").strip()
            model           = request.form.get("model", "gpt-4o").strip()
            conversation_id = request.form.get("conversation_id", "").strip()
            agent_note      = request.form.get("agent_note", "You are a helpful assistant.").strip()
            file            = request.files.get("file")

            if not question:
                raise ValueError("Please enter a question.")
            if len(question) > 2000:
                raise ValueError("Question too long.")

            # 2) file upload
            if file and file.filename:
                if not allowed_file(file.filename):
                    raise ValueError("File type not allowed.")
                safe_name = secure_filename(file.filename)
                save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)
                file.save(save_path)
                # TODO: process uploaded file

            # 3) conversation history
            if not conversation_id:
                conversation_id = str(uuid.uuid4())
            record = Conversation.query.get(conversation_id)
            if record:
                try:
                    history = json.loads(record.messages)
                except (json.JSONDecodeError, TypeError):
                    history = [{"role": "system", "content": agent_note}]
            else:
                history = [{"role": "system", "content": agent_note}]

            history.append({"role": "user", "content": question})

            # 4) call OpenAI
            try:
                resp = openai.ChatCompletion.create(
                    model=model,
                    messages=history,
                    timeout=15
                )
            except Exception as e:
                current_app.logger.error(f"OpenAI error: {e}")
                return render_template("ask_gptv2.html", error="AI service error."), 502

            answer = resp.choices[0].message.content.strip()
            history.append({"role": "assistant", "content": answer})

            # 5) save conversation
            if record:
                record.messages = json.dumps(history)
            else:
                record = Conversation(id=conversation_id, messages=json.dumps(history))
                db.session.add(record)
            db.session.commit()

            # 6) reload all for sidebar
            conversations = {}
            for conv in Conversation.query.all():
                try:
                    conversations[conv.id] = json.loads(conv.messages)
                except json.JSONDecodeError:
                    continue

            return render_template(
                "ask_gptv2.html",
                answer=format_answer(answer),
                conversations=conversations,
                conversation_id=conversation_id
            )

        except Exception as e:
            current_app.logger.error(f"/fun POST error: {e}")
            return render_template("ask_gptv2.html", error=str(e)), 400

    # GET: list existing conversations
    conversations = {}
    for conv in Conversation.query.all():
        try:
            conversations[conv.id] = json.loads(conv.messages)
        except json.JSONDecodeError:
            continue
    return render_template("ask_gptv2.html", conversations=conversations)


# dive-site routes below
@app.route('/dive-site')
def dive_site_index():
    return render_template('dive-site/home.html')

@app.route('/dive-site/about')
def dive_site_about():
    return render_template('dive-site/about.html')

@app.route('/dive-site/contact')
def dive_site_contact():
    return render_template('dive-site/contact.html')

@app.route('/dive-site/destinations')
def dive_site_destinations():
    return render_template('dive-site/destinations.html')

@app.route('/dive-site/indonesia')
def dive_site_indonesia():
    return render_template('dive-site/indonesia.html')

@app.route('/dive-site/maldives')
def dive_site_maldives():
    return render_template('dive-site/maldives.html')

@app.route('/dive-site/galapagos')
def dive_site_galapagos():
    return render_template('dive-site/galapagos.html')

@app.route('/dive-site/french-polynesia')
def dive_site_french_polynesia():
    return render_template('dive-site/french-polynesia.html')

@app.route('/dive-site/papua-new-guinea')
def dive_site_papua_new_guinea():
    return render_template('dive-site/papua-new-guinea.html')

@app.route('/dive-site/fiji')
def dive_site_fiji():
    return render_template('dive-site/fiji.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('404.html'), 500

if __name__ == '__main__':
    app.run(debug=False)
