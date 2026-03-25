from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
import os
import uuid
import httpx
from datetime import datetime
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI(title="Divine Encounter 2026 API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Load environment variables from .env file
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "your_supabase_url")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your_supabase_key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY)


# Paystack Configuration
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_your_secret_key")
PAYSTACK_API_URL = "https://api.paystack.co"

# Request Models
class RegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    attendance_mode: str
    church: Optional[str] = None
    special_needs: Optional[str] = None
    newsletter: bool = False

class PaymentVerificationRequest(BaseModel):
    reference: str


# ─── Page Routes ───────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/leaders", response_class=HTMLResponse)
async def leaders_page(request: Request):
    return templates.TemplateResponse("leaders.html", {"request": request})

@app.get("/mission", response_class=HTMLResponse)
async def mission_page(request: Request):
    return templates.TemplateResponse("mission.html", {"request": request})

@app.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request})

@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


# ─── API Routes ────────────────────────────────────────────────────────────────

@app.get("/api/stats")
async def get_stats():
    """Get registration statistics (for admin dashboard)"""
    try:
        total = supabase.table("registrations").select("id", count="exact").execute()
        paid = supabase.table("registrations")\
            .select("id", count="exact")\
            .eq("payment_status", "paid")\
            .execute()
        in_person = supabase.table("registrations")\
            .select("id", count="exact")\
            .eq("attendance_mode", "in-person")\
            .eq("payment_status", "paid")\
            .execute()

        return {
            "total_registrations": total.count,
            "paid_registrations": paid.count,
            "in_person_attendees": in_person.count,
            "virtual_attendees": paid.count - in_person.count if paid.count else 0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)