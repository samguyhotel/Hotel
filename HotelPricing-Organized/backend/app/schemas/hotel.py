from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


# Base Hotel Schema
class HotelBase(BaseModel):
    name: str
    address: str
    city: str
    state: Optional[str] = None
    country: str
    zip_code: Optional[str] = None
    currency: str = "USD"
    timezone: str = "UTC"
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    monthly_fixed_costs: float = 0.0


# Schema for creating a hotel
class HotelCreate(HotelBase):
    pass


# Schema for updating a hotel
class HotelUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    monthly_fixed_costs: Optional[float] = None
    is_active: Optional[bool] = None


# Schema for hotel response
class HotelResponse(HotelBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Room Type Base Schema
class RoomTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: float
    variable_cost: float
    inventory_count: int
    max_occupancy: int = 2
    amenities: Optional[str] = None
    image_url: Optional[str] = None


# Schema for creating a room type
class RoomTypeCreate(RoomTypeBase):
    hotel_id: int


# Schema for updating a room type
class RoomTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    variable_cost: Optional[float] = None
    inventory_count: Optional[int] = None
    max_occupancy: Optional[int] = None
    amenities: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


# Schema for room type response
class RoomTypeResponse(RoomTypeBase):
    id: int
    hotel_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Schema for detailed hotel response with room types
class HotelDetailResponse(HotelResponse):
    room_types: List[RoomTypeResponse] = []
