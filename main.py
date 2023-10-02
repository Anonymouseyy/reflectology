from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
import datetime, requests
from deta import Deta

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Initialize
deta = Deta()
entries_db = deta.Base("entries")
entries_drive = deta.Drive("entries")


@app.route("/", methods=["GET", "POST"])
def index():
    """Home Page"""
    q = requests.get("https://zenquotes.io/api/today").json()[0]

    return render_template("index.html", quote=q)


@app.route("/create", methods=["POST"])
def create():
    """Endpoint for creating an entry"""
    key = str(datetime.date.today())

    if entries_db.get(key) is None:
        flash("You already have an entry for today.")
        return redirect("/")

    data = {
        "title": "",
        "desc": "Today I...",
        "people": [],
        "places": [],
        "file": f"{key}.json"
    }

    default_entry = """
        {
            "ops": [
                 {       
                    "insert": "Today I..."
                }
            ]
        }"""

    entries_db.put(data, key)
    entries_drive.put(f"{key}.json", default_entry, "/")
