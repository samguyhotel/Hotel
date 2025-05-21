from typing import List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hotel import Hotel, RoomType, RoomPricing, PricingRule
from app.schemas.pricing import (
    PricingRuleCreate, PricingRuleUpdate, PricingRuleResponse,
    RoomPricingCreate, RoomPricingUpdate, RoomPricingResponse,
    PriceOverrideRequest, HotelPricingRecommendations,
    PriceElasticityRequest, PriceElasticitySimulation
)
from app.services.pricing import DynamicPricingEngine

router = APIRouter()


# Pricing Rules Endpoints

@router.post("/rules", response_model=PricingRuleResponse)
def create_pricing_rule(
    rule_in: PricingRuleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new pricing rule.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == rule_in.hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {rule_in.hotel_id} not found"
        )
    
    # Check if rule with same name already exists for this hotel
    existing_rule = db.query(PricingRule).filter(
        PricingRule.hotel_id == rule_in.hotel_id,
        PricingRule.name == rule_in.name
    ).first()
    
    if existing_rule:
        raise HTTPException(
            status_code=400,
            detail=f"Pricing rule '{rule_in.name}' already exists for this hotel"
        )
    
    # Create new pricing rule
    db_rule = PricingRule(
        hotel_id=rule_in.hotel_id,
        name=rule_in.name,
        description=rule_in.description,
        min_price_multiplier=rule_in.min_price_multiplier,
        max_price_multiplier=rule_in.max_price_multiplier,
        low_demand_threshold=rule_in.low_demand_threshold,
        high_demand_threshold=rule_in.high_demand_threshold
    )
    
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    
    return db_rule


@router.get("/rules", response_model=List[PricingRuleResponse])
def get_pricing_rules(
    hotel_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """
    Get all pricing rules, with optional filtering by hotel.
    """
    query = db.query(PricingRule)
    
    if hotel_id is not None:
        query = query.filter(PricingRule.hotel_id == hotel_id)
    
    if is_active is not None:
        query = query.filter(PricingRule.is_active == is_active)
    
    rules = query.offset(skip).limit(limit).all()
    return rules


@router.get("/rules/{rule_id}", response_model=PricingRuleResponse)
def get_pricing_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific pricing rule.
    """
    rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=404,
            detail=f"Pricing rule with ID {rule_id} not found"
        )
    
    return rule


@router.put("/rules/{rule_id}", response_model=PricingRuleResponse)
def update_pricing_rule(
    rule_id: int,
    rule_in: PricingRuleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a pricing rule's information.
    """
    rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=404,
            detail=f"Pricing rule with ID {rule_id} not found"
        )
    
    # Update rule attributes
    for field, value in rule_in.dict(exclude_unset=True).items():
        setattr(rule, field, value)
    
    db.commit()
    db.refresh(rule)
    
    return rule


@router.delete("/rules/{rule_id}", response_model=PricingRuleResponse)
def delete_pricing_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a pricing rule (soft delete by setting is_active to False).
    """
    rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
    if not rule:
        raise HTTPException(
            status_code=404,
            detail=f"Pricing rule with ID {rule_id} not found"
        )
    
    # Soft delete
    rule.is_active = False
    db.commit()
    db.refresh(rule)
    
    return rule


# Room Pricing Endpoints

@router.get("/room-pricing", response_model=List[RoomPricingResponse])
def get_room_pricing(
    room_type_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get room pricing data with optional filtering.
    """
    query = db.query(RoomPricing)
    
    if room_type_id is not None:
        query = query.filter(RoomPricing.room_type_id == room_type_id)
    
    if start_date is not None:
        query = query.filter(RoomPricing.date >= start_date)
    
    if end_date is not None:
        query = query.filter(RoomPricing.date <= end_date)
    
    pricing_data = query.offset(skip).limit(limit).all()
    return pricing_data


@router.post("/override", response_model=dict)
def override_price(
    override_in: PriceOverrideRequest,
    db: Session = Depends(get_db)
):
    """
    Apply a manual price override for a specific room on a specific date.
    """
    # Check if room type exists
    room_type = db.query(RoomType).filter(RoomType.id == override_in.room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=404,
            detail=f"Room type with ID {override_in.room_type_id} not found"
        )
    
    # Initialize pricing engine
    pricing_engine = DynamicPricingEngine(db)
    
    # Apply override
    result = pricing_engine.apply_price_override(
        room_type_id=override_in.room_type_id,
        date=override_in.date,
        price=override_in.price,
        notes=override_in.notes
    )
    
    return result


@router.get("/recommendations/{hotel_id}", response_model=HotelPricingRecommendations)
def get_pricing_recommendations(
    hotel_id: int,
    start_date: Optional[date] = None,
    days: int = 30,
    room_type_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Generate pricing recommendations for all room types in a hotel.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Use current date if start_date not provided
    if start_date is None:
        start_date = datetime.now().date()
    
    # Initialize pricing engine
    pricing_engine = DynamicPricingEngine(db)
    
    # Generate recommendations
    recommendations = pricing_engine.generate_pricing_recommendations(
        hotel_id=hotel_id,
        start_date=start_date,
        days=days,
        room_type_id=room_type_id
    )
    
    return recommendations


@router.post("/save-recommendations/{hotel_id}")
def save_pricing_recommendations(
    hotel_id: int,
    recommendations: HotelPricingRecommendations,
    db: Session = Depends(get_db)
):
    """
    Save pricing recommendations to the database.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Initialize pricing engine
    pricing_engine = DynamicPricingEngine(db)
    
    # Save recommendations
    pricing_engine.save_pricing_recommendations(
        hotel_id=hotel_id,
        recommendations=recommendations
    )
    
    return {"status": "success", "message": "Pricing recommendations saved successfully"}


@router.post("/elasticity", response_model=PriceElasticitySimulation)
def simulate_price_elasticity(
    elasticity_in: PriceElasticityRequest,
    db: Session = Depends(get_db)
):
    """
    Simulate price elasticity by predicting demand at different price points.
    """
    # Check if room type exists
    room_type = db.query(RoomType).filter(RoomType.id == elasticity_in.room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=404,
            detail=f"Room type with ID {elasticity_in.room_type_id} not found"
        )
    
    # Initialize pricing engine
    pricing_engine = DynamicPricingEngine(db)
    
    # Get hotel ID
    hotel_id = room_type.hotel_id
    
    # Simulate elasticity
    result = pricing_engine.forecaster.simulate_price_elasticity(
        hotel_id=hotel_id,
        room_type_id=elasticity_in.room_type_id,
        date=elasticity_in.date,
        price_range=elasticity_in.price_range
    )
    
    return result
