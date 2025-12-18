from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class FindApartmentRequest(BaseModel):
    """Request model for finding an apartment"""
    query: str


class AddUserRequest(BaseModel):
    """Request model for adding a user"""
    user_id: Optional[str] = None


class AddAppointmentRequest(BaseModel):
    """Request model for adding an appointment"""
    appointment_id: Optional[str] = None


class GetApartmentInfoRequest(BaseModel):
    """Request model for getting apartment info"""
    apartment_id: int


class GetApartmentQualificationRequest(BaseModel):
    """Request model for getting apartment qualification"""
    apartment_id: int


class GetScheduleRequest(BaseModel):
    """Request model for getting apartment schedule"""
    apartment_id: int


class SlotWithScore(BaseModel):
    """Model for a time slot with its booking score"""
    datetime: str = Field(description="Slot datetime in format DD-MM-YYYY HH:MM")
    score: int = Field(description="Booking score from 0-100, where 0 means shouldn't book and 100 means perfect slot")


class ScheduleResponse(BaseModel):
    """Response model for apartment schedule"""
    apartment_id: int
    apartment_name: str
    slots_available: List[SlotWithScore]


class SuccessResponse(BaseModel):
    """Standard success response model"""
    status: str
    message: str


class ApartmentData(BaseModel):
    """Apartment data model"""
    id: Optional[int] = None
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    price: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    sqft: Optional[int] = None
    description: Optional[str] = None


class GeminiApartmentResponse(BaseModel):
    """Simplified response model for Gemini AI (supports single or multiple apartment IDs)"""
    exists: bool = Field(description="True if matching apartments exist in the list, False otherwise")
    apartment_ids: List[int] = Field(
        default_factory=list,
        description="List of apartment IDs that match the query. Return a single ID for specific queries, multiple IDs for general queries. Return empty list if no matches found."
    )
    
    model_config = {"arbitrary_types_allowed": True}


class FindApartmentResponse(BaseModel):
    """Response model for finding an apartment"""
    exists: bool = Field(description="True if a matching apartment exists in the list, False otherwise")
    apartment_id: Optional[int] = Field(
        default=None,
        description="The ID of the apartment found (or attempted to find). Return the ID even if exists is False"
    )
    apartment: Optional[ApartmentData] = Field(
        default=None,
        description="Full apartment data when exists is True, null when exists is False"
    )
    message: Optional[str] = Field(
        default=None,
        description="Message indicating apartment does not exist when exists is False"
    )
    
    model_config = {"arbitrary_types_allowed": True}

