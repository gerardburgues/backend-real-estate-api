import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.ai_service import AIService
from models.schemas import (
    FindApartmentRequest,
    AddUserRequest,
    AddAppointmentRequest,
    GetApartmentInfoRequest,
    GetApartmentQualificationRequest,
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


@app.post("/tool/find-apartment")
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


@app.post("/tool/get-apartments")
async def get_apartments():
    """
    Get all apartments with basic info (name, street, city, and ref_code).
    """
    apartments = load_apartments()
    # Return name, street, city, and ref_code for each apartment
    basic_apartments = [
        {
            "name": apt.get("name"),
            "street": apt.get("street"),
            "city": apt.get("city"),
            "ref_code": apt.get("id")
        }
        for apt in apartments
    ]
    return {"apartments": basic_apartments}


@app.post("/tool/get-apartment-info")
async def get_apartment_info(request: GetApartmentInfoRequest):
    """
    Get apartment information by ID with is_qualification flag.
    
    Args:
        request: Request containing apartment_id
        
    Returns:
        Full apartment information with is_qualification boolean
        
    Raises:
        HTTPException: 404 if apartment not found
    """
    apartments = load_apartments()
    
    # Find apartment by ID
    apartment = None
    for apt in apartments:
        if apt.get("id") == request.apartment_id:
            apartment = apt.copy()
            break
    
    if not apartment:
        raise HTTPException(
            status_code=404,
            detail=f"Apartment with ID {request.apartment_id} not found"
        )
    
    # Add is_qualification flag (remove qualification from response)
    is_qualification = "qualification" in apartment and apartment.get("qualification") is not None
    apartment_with_flag = {k: v for k, v in apartment.items() if k != "qualification"}
    apartment_with_flag["is_qualification"] = is_qualification
    
    return apartment_with_flag


@app.post("/tool/get-apartment-qualification")
async def get_apartment_qualification(request: GetApartmentQualificationRequest):
    """
    Get apartment information by ID with full qualification details.
    
    Args:
        request: Request containing apartment_id
        
    Returns:
        Full apartment information including qualification details
        
    Raises:
        HTTPException: 404 if apartment not found
    """
    apartments = load_apartments()
    
    # Find apartment by ID
    apartment = None
    for apt in apartments:
        if apt.get("id") == request.apartment_id:
            apartment = apt
            break
    
    if not apartment:
        raise HTTPException(
            status_code=404,
            detail=f"Apartment with ID {request.apartment_id} not found"
        )
    
    return apartment


@app.get("/")
async def root():
    """Root endpoint - redirects to API documentation"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

