from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from draw_calendar import draw_calendar
import os.path
import json
from display_eink import update_eink

app = Flask(__name__)
events_path = "events.json"

# Save json data
def save_events(data, path):
    try:
        print("Saving events")
        with open(path, 'w') as file:
            data = json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error writing to file: {e}")

# Load json data
def load_events(path):
    try:
        print("Loading events")
        with open(path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
        return []

def sort_events(events):
    # Convert date strings to datetime for sorting
    return sorted(events, key=lambda e: datetime.strptime(e['date'], '%Y-%m-%d'))


# NEED TO CREATE THE STATIC DIRECTORY ASWELL
# MAke the folder if not found

# Check if events exist
if not os.path.exists(events_path):
    # Create an empty json
    print(f"{events_path} does not exist.")
    save_events([], events_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Load events
    events = load_events(events_path)

    # Add a new event
    if request.method == 'POST':
        date = request.form.get("date")
        title = request.form.get("title")

        if title and date:
            events.append({"title": title, "date": date})
            save_events(events, events_path)
        
        return redirect(url_for("index"))
    

    events = sort_events(events)
    draw_calendar(datetime.now(), events, 'static/calendar_display.png')
    update_eink('static/calendar_display.png')
    return render_template("index.html", events=events)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )