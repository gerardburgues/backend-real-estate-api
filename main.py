import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.ai_service import AIService
from models.schemas import (
    FindApartmentRequest,
    FindApartmentResponse,
    AddUserRequest,
    AddAppointmentRequest,
    GetApartmentInfoRequest,
    GetApartmentQualificationRequest,
    CheckScheduleRequest,
    CheckScheduleResponse,
    AvailableSlot,
    ScoreBreakdown,
    SuccessResponse,
)
from utils.apartment_loader import load_apartments
from utils.calendar_init import init_mock_calendar
from services.calendar_service import calendar_service
from datetime import date

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

# Initialize mock calendar data for testing
init_mock_calendar()


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


@app.post("/tool/check-schedule", response_model=CheckScheduleResponse)
async def check_schedule(request: CheckScheduleRequest):
    """
    Check available schedule slots for a property and return scored options.
    
    Args:
        request: Request containing apartment_id, optional start_date and days
        
    Returns:
        List of available slots with scores, sorted by score (highest first)
        
    Raises:
        HTTPException: 400 if invalid date format, 404 if apartment not found
    """
    # Validate apartment exists
    apartments = load_apartments()
    apartment_exists = any(apt.get("id") == request.apartment_id for apt in apartments)
    
    if not apartment_exists:
        raise HTTPException(
            status_code=404,
            detail=f"Apartment with ID {request.apartment_id} not found"
        )
    
    # Parse start_date if provided
    start_date_obj = None
    if request.start_date:
        try:
            start_date_obj = date.fromisoformat(request.start_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date format. Expected YYYY-MM-DD, got {request.start_date}"
            )
    
    # Find available slots with scores
    available_slots_data = calendar_service.find_available_slots(
        apartment_id=request.apartment_id,
        start_date=start_date_obj,
        days=request.days
    )
    
    # Convert to response models
    available_slots = [
        AvailableSlot(
            date=slot["date"],
            time=slot["time"],
            is_today=slot["is_today"],
            score=slot["score"],
            breakdown=ScoreBreakdown(**slot["breakdown"])
        )
        for slot in available_slots_data
    ]
    
    # Get best option (first one since they're sorted by score)
    best_option = available_slots[0] if available_slots else None
    
    return CheckScheduleResponse(
        apartment_id=request.apartment_id,
        available_slots=available_slots,
        total_available=len(available_slots),
        best_option=best_option
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

