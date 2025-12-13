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


@app.get("/apartments")
async def get_apartments():
    """
    Get all apartments with basic info (name, street, and reference).
    """
    apartments = load_apartments()
    # Return name, street, and reference (id) for each apartment
    basic_apartments = [
        {
            "name": apt.get("name"),
            "street": apt.get("street"),
            "reference": apt.get("id")
        }
        for apt in apartments
    ]
    return {"apartments": basic_apartments}


@app.get("/apartments/{apartment_id}")
async def get_apartment_by_id(apartment_id: int):
    """
    Get apartment details by ID including qualification rules.
    
    Args:
        apartment_id: The ID of the apartment to retrieve
        
    Returns:
        Full apartment information including qualification rules
        
    Raises:
        HTTPException: 404 if apartment not found
    """
    apartments = load_apartments()
    
    # Find apartment by ID
    apartment = None
    for apt in apartments:
        if apt.get("id") == apartment_id:
            apartment = apt
            break
    
    if not apartment:
        raise HTTPException(
            status_code=404,
            detail=f"Apartment with ID {apartment_id} not found"
        )
    
    return apartment


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

