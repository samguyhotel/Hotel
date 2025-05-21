from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field


# Pricing Rule Base Schema
class PricingRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    min_price_multiplier: float = Field(0.5, ge=0.0, le=1.0)
    max_price_multiplier: float = Field(2.0, ge=1.0)
    low_demand_threshold: float = Field(0.3, ge=0.0, le=1.0)
    high_demand_threshold: float = Field(0.7, ge=0.0, le=1.0)


# Schema for creating a pricing rule
class PricingRuleCreate(PricingRuleBase):
    hotel_id: int


# Schema for updating a pricing rule
class PricingRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    min_price_multiplier: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_price_multiplier: Optional[float] = Field(None, ge=1.0)
    low_demand_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    high_demand_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_active: Optional[bool] = None


# Schema for pricing rule response
class PricingRuleResponse(PricingRuleBase):
    id: int
    hotel_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Room Pricing Base Schema
class RoomPricingBase(BaseModel):
    room_type_id: int
    date: date
    suggested_price: float
    final_price: float
    is_override: bool = False
    override_notes: Optional[str] = None
    forecasted_demand: Optional[float] = None
    forecasted_occupancy: Optional[float] = None


# Schema for creating room pricing
class RoomPricingCreate(RoomPricingBase):
    pass


# Schema for updating room pricing
class RoomPricingUpdate(BaseModel):
    suggested_price: Optional[float] = None
    final_price: Optional[float] = None
    is_override: Optional[bool] = None
    override_notes: Optional[str] = None
    forecasted_demand: Optional[float] = None
    forecasted_occupancy: Optional[float] = None


# Schema for room pricing response
class RoomPricingResponse(RoomPricingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


# Schema for price override request
class PriceOverrideRequest(BaseModel):
    room_type_id: int
    date: date
    price: float
    notes: Optional[str] = None


# Schema for price recommendation
class PriceRecommendation(BaseModel):
    date: str
    room_type_id: int
    room_type_name: str
    base_price: float
    variable_cost: float
    demand_probability: float
    price_multiplier: float
    suggested_price: float
    final_price: float
    is_override: bool
    override_notes: Optional[str] = None
    contribution_margin: float
    contribution_margin_percentage: float
    expected_occupancy: float
    expected_bookings: float
    expected_revenue: float
    expected_contribution: float


# Schema for room type pricing recommendations
class RoomTypePricingRecommendations(BaseModel):
    room_type_id: int
    room_type_name: str
    base_price: float
    variable_cost: float
    inventory_count: int
    prices: List[PriceRecommendation]


# Schema for hotel pricing recommendations
class HotelPricingRecommendations(BaseModel):
    hotel_id: int
    start_date: str
    days: int
    generated_at: str
    recommendations: Dict[str, RoomTypePricingRecommendations]


# Schema for price elasticity data point
class PriceElasticityPoint(BaseModel):
    price: float
    demand_probability: float
    contribution_margin: float
    expected_revenue: float
    expected_contribution: float


# Schema for price elasticity simulation
class PriceElasticitySimulation(BaseModel):
    date: str
    elasticity: List[PriceElasticityPoint]


# Schema for price elasticity request
class PriceElasticityRequest(BaseModel):
    room_type_id: int
    date: date
    price_range: List[float] = Field(..., min_items=2, max_items=20)
