from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# السماح لتطبيق Flutter بالاتصال
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يفضل لاحقًا تحدد دومين معين
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مسار ملف الصلاحيات المؤقت
PERMISSIONS_FILE = "data/permissions.json"

# تحميل البيانات من JSON
def load_permissions():
    if not os.path.exists(PERMISSIONS_FILE):
        return []
    with open(PERMISSIONS_FILE, "r") as f:
        return json.load(f)

@app.post("/check_permission")
def check_permission(email: str = Form(...), video: str = Form(...)):
    permissions = load_permissions()
    for entry in permissions:
        if entry["email"] == email and entry["video"] == video:
            return {"allowed": True}
    return {"allowed": False}

@app.get("/")
def root():
    return {"status": "Doctor Smart API is running ✅"}
