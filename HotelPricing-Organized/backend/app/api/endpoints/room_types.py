from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hotel import RoomType, Hotel
from app.schemas.hotel import RoomTypeCreate, RoomTypeUpdate, RoomTypeResponse

router = APIRouter()


@router.post("/", response_model=RoomTypeResponse)
def create_room_type(
    room_type_in: RoomTypeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new room type.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == room_type_in.hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {room_type_in.hotel_id} not found"
        )
    
    # Check if room type with same name already exists for this hotel
    existing_room_type = db.query(RoomType).filter(
        RoomType.hotel_id == room_type_in.hotel_id,
        RoomType.name == room_type_in.name
    ).first()
    
    if existing_room_type:
        raise HTTPException(
            status_code=400,
            detail=f"Room type '{room_type_in.name}' already exists for this hotel"
        )
    
    # Create new room type
    db_room_type = RoomType(
        hotel_id=room_type_in.hotel_id,
        name=room_type_in.name,
        description=room_type_in.description,
        base_price=room_type_in.base_price,
        variable_cost=room_type_in.variable_cost,
        inventory_count=room_type_in.inventory_count,
        max_occupancy=room_type_in.max_occupancy,
        amenities=room_type_in.amenities,
        image_url=room_type_in.image_url
    )
    
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    
    return db_room_type


@router.get("/", response_model=List[RoomTypeResponse])
def get_room_types(
    hotel_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """
    Get all room types, with optional filtering by hotel.
    """
    query = db.query(RoomType)
    
    if hotel_id is not None:
        query = query.filter(RoomType.hotel_id == hotel_id)
    
    if is_active is not None:
        query = query.filter(RoomType.is_active == is_active)
    
    room_types = query.offset(skip).limit(limit).all()
    return room_types


@router.get("/{room_type_id}", response_model=RoomTypeResponse)
def get_room_type(
    room_type_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific room type.
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=404,
            detail=f"Room type with ID {room_type_id} not found"
        )
    
    return room_type


@router.put("/{room_type_id}", response_model=RoomTypeResponse)
def update_room_type(
    room_type_id: int,
    room_type_in: RoomTypeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a room type's information.
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=404,
            detail=f"Room type with ID {room_type_id} not found"
        )
    
    # Update room type attributes
    for field, value in room_type_in.dict(exclude_unset=True).items():
        setattr(room_type, field, value)
    
    db.commit()
    db.refresh(room_type)
    
    return room_type


@router.delete("/{room_type_id}", response_model=RoomTypeResponse)
def delete_room_type(
    room_type_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a room type (soft delete by setting is_active to False).
    """
    room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not room_type:
        raise HTTPException(
            status_code=404,
            detail=f"Room type with ID {room_type_id} not found"
        )
    
    # Soft delete
    room_type.is_active = False
    db.commit()
    db.refresh(room_type)
    
    return room_type
