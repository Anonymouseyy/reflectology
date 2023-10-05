from flask import Flask, flash, redirect, render_template, request, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import datetime, requests, random
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
    entries = entries_db.fetch().items
    entries.sort(key=lambda x: x["date"], reverse=True)
    formatted_entries = []

    for entry in entries:
        day = datetime.date.fromisoformat(entry['date'])
        suf = "th"

        if day.day in [1, 21, 31]:
            suf = "st"
        elif day.day in [2, 22]:
            suf = "nd"
        elif day.day in [3, 23]:
            suf = "rd"

        if entry["date"] == str(datetime.date.today()):
            display_title = "Today, " + day.strftime("%B ") + str(day.day) + suf + f": {entry['title']}"
        elif entry["date"] == str(datetime.date.today() - datetime.timedelta(days=1)):
            display_title = "Yesterday, " + day.strftime("%B ") + str(day.day) + suf + f": {entry['title']}"
        else:
            display_title = day.strftime("%A, %B ") + str(day.day) + suf + f": {entry['title']}"

        data = {
            "key": entry["key"],
            "display_title": display_title,
            "desc": entry["desc"]
        }

        formatted_entries.append(data)

    return render_template("index.html", quote=q, entries=formatted_entries)


@app.route("/create", methods=["GET"])
def create():
    """Endpoint for creating an entry"""
    adjectives = [
        "Massive",
        "Great",
        "Stellar",
        "Amazing",
        "Cool",
        "Fantastic"
    ]
    adjectives2 = [
        "Monkey",
        "Crazy",
        "Bright",
        "Sunny",
        "Beautiful",
        "Majestic"
    ]
    nouns = [
        "Adventure",
        "Journey",
        "Mission",
        "Innovation",
        "Creation",
        "Day"
    ]

    title = f"The {random.choice(adjectives)} {random.choice(adjectives2)} {random.choice(nouns)}"

    date = str(datetime.date.today())

    data = {
        "date": date,
        "title": title,
        "desc": "Today I...",
        "people": [],
        "places": [],
        "file": ""
    }

    default_entry = """
        {
            "ops": [
                 {       
                    "insert": "Today I..."
                }
            ]
        }"""

    key = entries_db.put(data)["key"]
    entries_drive.put(f"{key}.json", default_entry)
    entries_db.update({"file": f"{key}.json"}, key)

    return redirect(f"/edit?entry={key}")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    """Endpoint for editting an entry"""
    # Basic Displaying
    q = requests.get("https://zenquotes.io/api/today").json()[0]
    key = request.args["entry"]
    entry = entries_db.get(key)
    day = datetime.date.fromisoformat(entry['date'])
    suf = "th"

    if day.day in [1, 21, 31]:
        suf = "st"
    elif day.day in [2, 22]:
        suf = "nd"
    elif day.day in [3, 23]:
        suf = "rd"

    if entry["date"] == str(datetime.date.today()):
        entry["display_title"] = "Today, " + day.strftime("%B ") + str(day.day) + suf + ":"
    elif entry["date"] == str(datetime.date.today() - datetime.timedelta(days=1)):
        entry["display_title"] = "Yesterday, " + day.strftime("%B ") + str(day.day) + suf + ":"
    else:
        entry["display_title"] = day.strftime("%A, %B ") + str(day.day) + suf + ":"

    content = entries_drive.get(entry["file"]).read().decode()

    # Get ideas
    ideas_pared = []
    ideas = [
        "What am I proud of today?",
        "What am I grateful for today?",
        "What is a problem am I currently facing?",
        "What is something that I started today?",
        "Something fun I did today.",
        "What did I eat for lunch?",
        "What is something I accomplished today?",
        "Who is my best friend today?",
        "How do I feel right now?",
        "What are my thoughts on life right now?",
        "What did I learn today?",
        "What was the hardest thing I did today?",
        "Rant about something",
        "How will tomorrow be better?",
        "Who do I dislike the most today?"
    ]

    for i in range(5):
        ideas_pared.append(random.choice(ideas))
        ideas.remove(ideas_pared[i])

    # Getting reflection entry
    all_items = list(entries_db.fetch({"date?ne": entry['date']}).items)
    if all_items:
        reflection = random.choice(all_items)
    else:
        reflection = None

    return render_template("edit.html", entry=entry, content=content, quote=q, prompts=ideas_pared, reflection=reflection)


@app.route("/save", methods=["POST"])
def save():
    """Endpoint for saving an entry"""
    data = request.get_json()
    key = data[0]["key"]
    desc = data[3]["raw_content"]

    if len(desc) > 481:
        desc = desc[:478]+"..."

    updates = {
        "title": data[1]["title"],
        "desc": desc
    }

    if data[4]["date"]:
        updates["date"] = data[4]["date"]

    entries_db.update(updates, key)
    entries_drive.put(f"{key}.json", f"{data[2]['content']}")

    return jsonify({"res": "success"})


@app.route("/delete", methods=["POST"])
def delete():
    """Endpoint for deleting an entry"""
    key = request.form.get("entry")

    item = entries_db.get(key)
    entries_drive.delete(item["file"])
    entries_db.delete(key)

    return redirect("/")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
