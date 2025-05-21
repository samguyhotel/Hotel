from typing import List, Optional
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hotel import Hotel, RoomType
from app.schemas.forecasting import (
    DemandForecastRequest, DemandForecastResponse,
    ForecastModelTrainingRequest
)
from app.services.forecasting import DemandForecaster

router = APIRouter()


@router.post("/demand", response_model=DemandForecastResponse)
def forecast_demand(
    forecast_in: DemandForecastRequest,
    db: Session = Depends(get_db)
):
    """
    Generate demand forecast for a specific room type over a future period.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == forecast_in.hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {forecast_in.hotel_id} not found"
        )
    
    # Check if room type exists
    room_type = db.query(RoomType).filter(
        RoomType.id == forecast_in.room_type_id,
        RoomType.hotel_id == forecast_in.hotel_id
    ).first()
    
    if not room_type:
        raise HTTPException(
            status_code=404,
            detail=f"Room type with ID {forecast_in.room_type_id} not found for hotel ID {forecast_in.hotel_id}"
        )
    
    # Initialize forecaster
    forecaster = DemandForecaster(db)
    
    # Generate forecast
    forecast_data = forecaster.forecast_demand(
        hotel_id=forecast_in.hotel_id,
        room_type_id=forecast_in.room_type_id,
        start_date=forecast_in.start_date,
        days=forecast_in.days
    )
    
    # Calculate end date
    end_date = forecast_in.start_date + timedelta(days=forecast_in.days - 1)
    
    # Prepare response
    response = {
        "hotel_id": forecast_in.hotel_id,
        "room_type_id": forecast_in.room_type_id,
        "room_type_name": room_type.name,
        "start_date": forecast_in.start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "days": forecast_in.days,
        "generated_at": datetime.now().isoformat(),
        "forecast": forecast_data
    }
    
    return response


@router.post("/train-model")
def train_forecast_model(
    training_in: ForecastModelTrainingRequest,
    db: Session = Depends(get_db)
):
    """
    Train a forecasting model for a hotel or specific room type.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == training_in.hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {training_in.hotel_id} not found"
        )
    
    # If room_type_id provided, check if it exists
    if training_in.room_type_id:
        room_type = db.query(RoomType).filter(
            RoomType.id == training_in.room_type_id,
            RoomType.hotel_id == training_in.hotel_id
        ).first()
        
        if not room_type:
            raise HTTPException(
                status_code=404,
                detail=f"Room type with ID {training_in.room_type_id} not found for hotel ID {training_in.hotel_id}"
            )
    
    # Initialize forecaster
    forecaster = DemandForecaster(db)
    
    # Train models based on model_type
    if training_in.model_type in ["prophet", "combined"]:
        forecaster.train_prophet_model(
            hotel_id=training_in.hotel_id,
            room_type_id=training_in.room_type_id
        )
    
    if training_in.model_type in ["xgboost", "combined"]:
        forecaster.train_xgb_model(
            hotel_id=training_in.hotel_id,
            room_type_id=training_in.room_type_id
        )
    
    return {
        "status": "success",
        "message": f"Successfully trained {training_in.model_type} model for hotel ID {training_in.hotel_id}",
        "hotel_id": training_in.hotel_id,
        "room_type_id": training_in.room_type_id,
        "model_type": training_in.model_type,
        "trained_at": datetime.now().isoformat()
    }
