import os
from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
import httpx
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# MariaDB Config
MARIADB_USERNAME = os.getenv('DB_USERNAME') 
MARIADB_PASSWORD = os.getenv('DB_PASSWORD') 
MARIADB_HOST = os.getenv('DB_HOST', 'localhost')
MARIADB_PORT = os.getenv('DB_PORT')
MARIADB_DATABASE = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{MARIADB_USERNAME}:{MARIADB_PASSWORD}@{MARIADB_HOST}:{MARIADB_PORT}/{MARIADB_DATABASE}"
)

# Constants
OPENF1_BASE = "https://api.openf1.org/v1"
JOLPICA_BASE = "https://api.jolpi.ca/ergast/f1"

COUNTRY_CODE_MAP = {
    "Australia": "AU",
    "China": "CN",
    "Japan": "JP",
    "Bahrain": "BH",
    "Saudi Arabia": "SA",
    "USA": "US",
    "Italy": "IT",  
    "Monaco": "MC",
    "Spain": "ES",
    "Canada": "CA",
    "Austria": "AT",
    "UK": "GB",
    "Belgium": "BE",
    "Hungary": "HU",
    "Netherlands": "NL",
    "Azerbaijan": "AZ",
    "Singapore": "SG",
    "Mexico": "MX",
    "Brazil": "BR",
    "Qatar": "QA",
    "UAE": "AE",
}

session_definitions = [
    ("First Practice", "FirstPractice"),
    ("Second Practice", "SecondPractice"),
    ("Third Practice", "ThirdPractice"),
    ("Sprint Qualifying", "SprintQualifying"),
    ("Sprint", "Sprint"),
    ("Qualifying", "Qualifying")
]

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

# Functions


# Upgrade image resolution by removing transformation parameters from the URL
def upgrade_image_res(url):
    if url:
        # Remove all transformations in the URL
        return url.split(".transform/")[0]
    # If no transformations found, return the original URL
    return url

# Sort drivers by their team names and group them
def sort_drivers_by_team(drivers):
    teams = {}
    
    for driver in drivers:
        # Extract team name and color
        team_name = driver.get("team_name")
        team_color = driver.get("team_color")

        # Add team to dictionary if not already present
        if team_name not in teams:
            teams[team_name] = {
                "team_color": team_color,
                "drivers": []
            }
        
        # Append driver to the respective team
        teams[team_name]["drivers"].append(driver)

    # Convert dictionary to a list of teams for easier handling in frontend
    team_list = list(teams.values())
    return team_list

# Search list of meetings and compare dates with current date to find the next meeting
def get_next_meeting(meetings):
    now = datetime.now(timezone.utc)
    future_meetings = []

    for m in meetings:
        # Combine date and time (Jolpica splits them)
        dt_str = f"{m['date']}T{m['time']}"
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

        if dt >= now:
            m["formattedTime"] = dt.strftime("%H:%M UTC")
            future_meetings.append(m)

    return min(
        future_meetings,
        key=lambda m: datetime.fromisoformat(f"{m['date']}T{m['time']}".replace("Z", "+00:00")),
        default=None  # return None if no future meetings
    )

def sort_sessions_in_meeting(meeting):

    # Extract and sort sessions into session list
    sessions = []
    for session_name, session_key in session_definitions:
        if session_key in meeting:
            session_data = meeting.pop(session_key)
            sessions.append(
                {
                    "name": session_name,
                    "key": session_key,
                    "date": session_data["date"],
                    "time": session_data["time"],
                }
            )

    # Add the Race session separately as it is not returned as an indivdual session by jolpica, rather as the main meeting date/time
    sessions.append({
        "name": "Race",
        "key": "Race",
        "date": meeting.pop("date"),
        "time": meeting.pop("time"),
        "formattedTime": meeting.pop("formattedTime", None)
    })

    meeting['sessions'] = sessions
    print(meeting)

    return meeting

# Map country names to their respective ISO 3166-1 alpha-2 codes
def get_country_code(meeting):
    country = meeting['Circuit']['Location']['country']
    code = COUNTRY_CODE_MAP.get(country, "")
    meeting['countryCode'] = code
    return meeting




# App route for fetching and parsing driver data in customized json format
@app.route('/drivers')
def drivers():
    url = f"{OPENF1_BASE}/drivers?session_key=latest"
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            drivers = response.json()
            for driver in drivers:
                # Upgrade image resolution
                driver['headshot_url'] = upgrade_image_res(driver.get('headshot_url'))
                # Rename team_colour to team_color for consistency
                driver['team_color'] = driver.pop('team_colour')
            
            # Sort drivers by team
            sorted_drivers = sort_drivers_by_team(drivers)

            return jsonify(sorted_drivers)
        
    except httpx.HTTPStatusError as e:
        return jsonify({"error": "OpenF1 returned an error", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": "OpenF1 unreachable", "details": str(e)}), 503


# App route for fetching and the current or next grand prix weekend data
@app.route('/next-race')
def next_race():
    current_time = datetime.now(timezone.utc)

    url = (f"{JOLPICA_BASE}/current/races.json")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            res = client.get(url)
            res.raise_for_status()
            data = res.json()
            meetings = data['MRData']['RaceTable']['Races']

            next_meeting = get_next_meeting(meetings)

        if not next_meeting:
            return jsonify({"message": "No upcoming meetings found"}), 404
        
        # Add country code for flag display
        next_meeting = get_country_code(next_meeting)
        # Sort sessions in the meeting
        next_meeting = sort_sessions_in_meeting(next_meeting)

        return jsonify(next_meeting)

    except httpx.HTTPStatusError as e:
        return jsonify({"error": "Jolpicaf1 returned an error", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": "Jolpicaf1 unreachable", "details": str(e)}), 503

# App route for fetching and parsing track map svgs
@app.route('/track-maps/<circuit_id>.svg')
def get_track(circuit_id):
    return send_from_directory("static/track_svgs", f"{circuit_id}.svg")

    

if __name__ == "__main__":
    app.run(debug=True)
