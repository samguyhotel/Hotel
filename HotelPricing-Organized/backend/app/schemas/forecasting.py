from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


# Schema for demand forecast data point
class DemandForecastPoint(BaseModel):
    date: str
    demand_probability: float
    prophet_forecast: Optional[float] = None
    xgb_forecast: Optional[float] = None


# Schema for demand forecast request
class DemandForecastRequest(BaseModel):
    hotel_id: int
    room_type_id: int
    start_date: date
    days: int = Field(90, ge=1, le=365)


# Schema for demand forecast response
class DemandForecastResponse(BaseModel):
    hotel_id: int
    room_type_id: int
    room_type_name: Optional[str] = None
    start_date: str
    end_date: str
    days: int
    generated_at: str
    forecast: List[DemandForecastPoint]


# Schema for external event
class ExternalEvent(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    impact_level: float = Field(..., ge=0.0, le=1.0)  # 0.0 to 1.0 impact on demand
    location: Optional[str] = None


# Schema for creating an external event
class ExternalEventCreate(ExternalEvent):
    hotel_id: int


# Schema for updating an external event
class ExternalEventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    impact_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    location: Optional[str] = None
    is_active: Optional[bool] = None


# Schema for external event response
class ExternalEventResponse(ExternalEvent):
    id: int
    hotel_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Schema for seasonality pattern
class SeasonalityPattern(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    multiplier: float = Field(..., ge=0.0)  # Multiplier for demand during this period
    recurrence: str = "yearly"  # yearly, monthly, weekly, once


# Schema for creating a seasonality pattern
class SeasonalityPatternCreate(SeasonalityPattern):
    hotel_id: int


# Schema for updating a seasonality pattern
class SeasonalityPatternUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    multiplier: Optional[float] = Field(None, ge=0.0)
    recurrence: Optional[str] = None
    is_active: Optional[bool] = None


# Schema for seasonality pattern response
class SeasonalityPatternResponse(SeasonalityPattern):
    id: int
    hotel_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Schema for historical booking data point
class HistoricalBookingPoint(BaseModel):
    date: date
    room_type_id: int
    total_rooms: int
    rooms_sold: int
    occupancy_rate: float
    average_daily_rate: float
    revenue: float


# Schema for importing historical booking data
class HistoricalBookingImport(BaseModel):
    hotel_id: int
    data: List[HistoricalBookingPoint]


# Schema for forecast model training request
class ForecastModelTrainingRequest(BaseModel):
    hotel_id: int
    room_type_id: Optional[int] = None  # If None, train for all room types
    model_type: str = "combined"  # prophet, xgboost, or combined
