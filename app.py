import os
import time
import json
import threading
from threading import Lock
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

from draw_calendar import draw_calendar
from display_eink import update_eink


# --------------------
# App setup
# --------------------

app = Flask(__name__)
events_path = "events.json"
image_path = "static/calendar_display.png"

display_lock = Lock()


# --------------------
# Event helpers
# --------------------

def save_events(data, path):
    try:
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error writing events file: {e}")


def load_events(path):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def sort_events(events):
    return sorted(events, key=lambda e: datetime.strptime(e["date"], "%Y-%m-%d"))


# --------------------
# Web route
# --------------------

@app.route("/", methods=["GET", "POST"])
def index():
    events = load_events(events_path)

    if request.method == "POST":
        date = request.form.get("date")
        title = request.form.get("title")

        if title and date:
            events.append({"title": title, "date": date})
            events = sort_events(events)
            save_events(events, events_path)

            # Update image + e-ink (real change)
            with display_lock:
                draw_calendar(datetime.now(), events, image_path)
                update_eink(image_path)

        return redirect(url_for("index"))

    # GET: only ensure the image exists for the website
    if not os.path.exists(image_path):
        draw_calendar(datetime.now(), events, image_path)

    return render_template("index.html", events=events)


# --------------------
# Midnight updater
# --------------------

def seconds_until_midnight():
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return (tomorrow - now).total_seconds()


def midnight_updater():
    while True:
        time.sleep(seconds_until_midnight())

        events = load_events(events_path)
        with display_lock:
            draw_calendar(datetime.now(), events, image_path)
            update_eink(image_path)


# --------------------
# Startup
# --------------------

if __name__ == "__main__":
    # Ensure required files/folders exist
    os.makedirs("static", exist_ok=True)

    if not os.path.exists(events_path):
        save_events([], events_path)

    # Start midnight background thread
    threading.Thread(
        target=midnight_updater,
        daemon=True
    ).start()

    # Start Flask server
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
