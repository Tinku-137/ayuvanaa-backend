from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = FastAPI()

# CORS setup to allow frontend on ayuvanaa.com
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ayuvanaa.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Sheet setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
gc = gspread.authorize(CREDS)
sheet = gc.open("Ayuvanaa User Data").sheet1  # Change to your sheet name

@app.post("/submit-registration")
async def submit_registration(request: Request):
    try:
        form = await request.form()
        form = dict(form)

        values = [
            form.get("name", ""),
            form.get("age", ""),
            form.get("gender", ""),
            form.get("phone", ""),
            form.get("language", ""),
            form.get("wake_time", ""),
            form.get("sleep_time", ""),
            form.get("exercise_time", ""),
            form.get("breakfast_time", ""),
            form.get("lunch_time", ""),
            form.get("dinner_time", ""),
            form.get("medicine_times", ""),
            form.get("medicine_reason", ""),
            form.get("health_condition", ""),
            form.get("others", ""),
            "Yes" if form.get("consent") else "No",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        sheet.append_row(values)
        return {"status": "success", "message": "User data saved successfully."}
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": "Failed to save user data."}
