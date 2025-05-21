from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hotel import Hotel
from app.models.hotel import RoomType
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse, HotelDetailResponse

router = APIRouter()


@router.post("/", response_model=HotelResponse)
def create_hotel(
    hotel_in: HotelCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new hotel.
    """
    # Check if hotel with same name already exists
    existing_hotel = db.query(Hotel).filter(Hotel.name == hotel_in.name).first()
    if existing_hotel:
        raise HTTPException(
            status_code=400,
            detail=f"Hotel with name '{hotel_in.name}' already exists"
        )
    
    # Create new hotel
    db_hotel = Hotel(
        name=hotel_in.name,
        address=hotel_in.address,
        city=hotel_in.city,
        state=hotel_in.state,
        country=hotel_in.country,
        zip_code=hotel_in.zip_code,
        currency=hotel_in.currency,
        timezone=hotel_in.timezone,
        logo_url=hotel_in.logo_url,
        primary_color=hotel_in.primary_color,
        secondary_color=hotel_in.secondary_color,
        monthly_fixed_costs=hotel_in.monthly_fixed_costs
    )
    
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    
    return db_hotel


@router.get("/", response_model=List[HotelResponse])
def get_hotels(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """
    Get all hotels, with optional filtering.
    """
    query = db.query(Hotel)
    
    if is_active is not None:
        query = query.filter(Hotel.is_active == is_active)
    
    hotels = query.offset(skip).limit(limit).all()
    return hotels


@router.get("/{hotel_id}", response_model=HotelDetailResponse)
def get_hotel(
    hotel_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific hotel.
    """
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Get room types for this hotel
    room_types = db.query(RoomType).filter(RoomType.hotel_id == hotel_id).all()
    
    # Create response with hotel and room types
    response = HotelDetailResponse(
        id=hotel.id,
        name=hotel.name,
        address=hotel.address,
        city=hotel.city,
        state=hotel.state,
        country=hotel.country,
        zip_code=hotel.zip_code,
        currency=hotel.currency,
        timezone=hotel.timezone,
        logo_url=hotel.logo_url,
        primary_color=hotel.primary_color,
        secondary_color=hotel.secondary_color,
        monthly_fixed_costs=hotel.monthly_fixed_costs,
        is_active=hotel.is_active,
        created_at=hotel.created_at,
        updated_at=hotel.updated_at,
        room_types=room_types
    )
    
    return response


@router.put("/{hotel_id}", response_model=HotelResponse)
def update_hotel(
    hotel_id: int,
    hotel_in: HotelUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a hotel's information.
    """
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Update hotel attributes
    for field, value in hotel_in.dict(exclude_unset=True).items():
        setattr(hotel, field, value)
    
    db.commit()
    db.refresh(hotel)
    
    return hotel


@router.delete("/{hotel_id}", response_model=HotelResponse)
def delete_hotel(
    hotel_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a hotel (soft delete by setting is_active to False).
    """
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Soft delete
    hotel.is_active = False
    db.commit()
    db.refresh(hotel)
    
    return hotel
