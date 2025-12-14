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


class CheckScheduleRequest(BaseModel):
    """Request model for checking available schedule slots"""
    apartment_id: int
    start_date: Optional[str] = Field(
        default=None,
        description="Start date for search (ISO format: YYYY-MM-DD). Defaults to today"
    )
    days: int = Field(
        default=7,
        description="Number of days to search ahead. Defaults to 7"
    )


class ScoreBreakdown(BaseModel):
    """Score breakdown for a time slot"""
    cluster_perfecto: int = Field(default=0, description="Cluster Perfecto bonus (+100)")
    urgencia_hoy: int = Field(default=0, description="Urgencia HOY bonus (+50, only for today)")
    efecto_ancla: int = Field(default=0, description="Efecto Ancla bonus (+20)")
    bloque_limpio: int = Field(default=0, description="Bloque Limpio bonus (+10)")
    cambio_turno: int = Field(default=0, description="Cambio de Turno penalty (-10)")
    cambio_intra_turno: int = Field(default=0, description="Cambio Intra-Turno penalty (-50)")
    romper_dia: int = Field(default=0, description="Romper el Día penalty (-80)")
    canibalizacion: int = Field(default=0, description="Canibalización penalty (-200)")


class AvailableSlot(BaseModel):
    """Available time slot with score"""
    date: str = Field(description="Date in ISO format (YYYY-MM-DD)")
    time: str = Field(description="Time slot (HH:MM)")
    is_today: bool = Field(description="Whether this slot is today")
    score: int = Field(description="Total score for this slot")
    breakdown: ScoreBreakdown = Field(description="Score breakdown")


class CheckScheduleResponse(BaseModel):
    """Response model for checking schedule"""
    apartment_id: int
    available_slots: List[AvailableSlot] = Field(
        description="List of available slots sorted by score (highest first)"
    )
    total_available: int = Field(description="Total number of available slots")
    best_option: Optional[AvailableSlot] = Field(
        default=None,
        description="Best scoring option (highest score)"
    )


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

