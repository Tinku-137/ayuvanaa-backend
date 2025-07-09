from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS setup to allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ayuvanaa.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Sheets setup
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
gc = gspread.authorize(CREDS)

# Main registration sheet
general_sheet = gc.open("Ayuvanaa User Data").sheet1
# Reminders sheet
reminders_sheet = gc.open("Ayuvanaa User Data").worksheet("Ayuvanaa Reminders Sheet")

@app.post("/submit-registration")
async def submit_registration(request: Request):
    try:
        form = await request.form()
        data = dict(form)

        # Save full data to general sheet
        general_values = [
            data.get("name", ""),
            data.get("age", ""),
            data.get("gender", ""),
            data.get("phone", ""),
            data.get("language", ""),
            data.get("wake_time", ""),
            data.get("sleep_time", ""),
            data.get("exercise_time", ""),
            data.get("breakfast_time", ""),
            data.get("lunch_time", ""),
            data.get("dinner_time", ""),
            data.get("medicine_times", ""),
            data.get("medicine_reason", ""),
            data.get("health_condition", ""),
            data.get("others", ""),
            "Yes" if data.get("consent") else "No",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ]
        general_sheet.append_row(general_values)

        # Prepare reminders data
        name = data.get("name", "")
        phone = data.get("phone", "")
        wake_time = data.get("wake_time", "")
        sleep_time = data.get("sleep_time", "")
        exercise_time = data.get("exercise_time", "")
        breakfast_time = data.get("breakfast_time", "")
        lunch_time = data.get("lunch_time", "")
        dinner_time = data.get("dinner_time", "")
        medicine_times = data.get("medicine_times", "")

        # Initial next message times same as user preferences
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rem_values = [
            name,
            phone,
            wake_time,
            sleep_time,
            exercise_time,
            breakfast_time,
            lunch_time,
            dinner_time,
            medicine_times,
            wake_time,       # next_wake_msg_time
            sleep_time,      # next_sleep_msg_time
            medicine_times,  # next_medicine_msg_time (could parse first time)
            now,             # last_msg_sent
            "pending",      # status
        ]
        reminders_sheet.append_row(rem_values)

        return {"status": "success", "message": "User registered successfully."}

    except Exception as e:
        logging.error(f"Error in registration: {e}")
        return {"status": "error", "message": str(e)}
