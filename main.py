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

    # Fetch returns objects in alphanumerical order
    entries = entries_db.fetch().items().reverse()
    formatted_entries = []

    for entry in entries:
        day = datetime.date.fromisoformat(entry['key'])
        suf = "th"

        if day.day in [1, 21, 31]:
            suf = "st"
        elif day.day in [2, 22]:
            suf = "nd"

        if entry["key"] == str(datetime.date.today()):
            display_title = "Today, " + day.strftime("%B %d") + suf + f": {entry['title']}"
        elif entry["key"] == str(datetime.date.today()-datetime.timedelta(days=1)):
            display_title = "Yesterday, " + day.strftime("%B %d") + suf + f": {entry['title']}"
        else:
            display_title = day.strftime("%A, %B %d") + suf + f": {entry['title']}"

        data = {
            "key": entry["key"],
            "display_title": display_title,
            "desc": entry["desc"]
        }

        formatted_entries.append(data)

    return render_template("index.html", quote=q, entries=formatted_entries)


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
