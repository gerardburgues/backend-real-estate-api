from pydantic import BaseModel
from typing import Optional


class FindApartmentRequest(BaseModel):
    """Request model for finding an apartment"""
    query: str


class AddUserRequest(BaseModel):
    """Request model for adding a user"""
    user_id: Optional[str] = None


class AddAppointmentRequest(BaseModel):
    """Request model for adding an appointment"""
    appointment_id: Optional[str] = None


class SuccessResponse(BaseModel):
    """Standard success response model"""
    status: str
    message: str

