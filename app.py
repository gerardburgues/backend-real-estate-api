import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.ai_service import AIService
from models.schemas import (
    FindApartmentRequest,
    AddUserRequest,
    AddAppointmentRequest,
    SuccessResponse,
)
from utils.apartment_loader import load_apartments

# Load environment variables
load_dotenv()

app = FastAPI(title="Real Estate Tool Calls API", version="1.0.0")

# Configure CORS for Vapi integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Service
ai_service = None
try:
    ai_service = AIService()
except ValueError:
    # Service will be None if API key is not configured
    # This is okay for endpoints that don't require AI
    pass


@app.post("/tool/find-apartment", response_model=dict)
async def find_apartment(request: FindApartmentRequest):
    """
    Find the best matching apartment based on user query using Gemini LLM.
    """
    if not ai_service:
        raise HTTPException(
            status_code=500, detail="GEMINI_API_KEY not configured"
        )
    
    apartments = load_apartments()
    selected_apartment = await ai_service.find_best_apartment(
        request.query, apartments
    )
    return selected_apartment


@app.post("/tool/add-user", response_model=SuccessResponse)
async def add_user(request: AddUserRequest):
    """
    Add user to the application.
    """
    print("HELLO WORLD")
    return SuccessResponse(
        status="success",
        message="added user to app"
    )


@app.post("/tool/add-appointment", response_model=SuccessResponse)
async def add_appointment(request: AddAppointmentRequest):
    """
    Add appointment to calendar.
    """
    print("ADDING TO CALENDAR")
    return SuccessResponse(
        status="success",
        message="added appointment to calendar"
    )


@app.get("/")
async def root():
    """Root endpoint - redirects to API documentation"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

