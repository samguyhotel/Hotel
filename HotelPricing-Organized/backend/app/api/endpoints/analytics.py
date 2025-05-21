from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract

from app.db.session import get_db
from app.models.hotel import Hotel, RoomType, RoomPricing

router = APIRouter()


@router.get("/revenue/{hotel_id}")
def get_revenue_analytics(
    hotel_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    room_type_id: Optional[int] = None,
    group_by: str = "day",  # day, week, month
    db: Session = Depends(get_db)
):
    """
    Get revenue analytics for a hotel.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().date()
    
    if not start_date:
        # Default to 30 days before end_date
        start_date = end_date - timedelta(days=30)
    
    # Build query for room types
    room_types_query = db.query(RoomType).filter(RoomType.hotel_id == hotel_id)
    if room_type_id:
        room_types_query = room_types_query.filter(RoomType.id == room_type_id)
    
    room_types = room_types_query.all()
    if not room_types:
        raise HTTPException(
            status_code=404,
            detail=f"No room types found for hotel ID {hotel_id}"
        )
    
    # Get room type IDs
    room_type_ids = [rt.id for rt in room_types]
    
    # Build query for pricing data
    query = db.query(
        RoomPricing.date,
        RoomPricing.room_type_id,
        RoomPricing.final_price,
        RoomPricing.forecasted_occupancy
    ).filter(
        RoomPricing.room_type_id.in_(room_type_ids),
        RoomPricing.date >= start_date,
        RoomPricing.date <= end_date
    )
    
    pricing_data = query.all()
    
    # Process data for analytics
    analytics_data = []
    room_type_dict = {rt.id: rt for rt in room_types}
    
    # Group data by date
    date_grouped_data = {}
    for item in pricing_data:
        date_key = item.date
        
        # Adjust key based on group_by parameter
        if group_by == "week":
            # Get the Monday of the week
            date_key = item.date - timedelta(days=item.date.weekday())
        elif group_by == "month":
            # Get the first day of the month
            date_key = date(item.date.year, item.date.month, 1)
        
        if date_key not in date_grouped_data:
            date_grouped_data[date_key] = []
        
        date_grouped_data[date_key].append(item)
    
    # Calculate analytics for each group
    for date_key, items in date_grouped_data.items():
        total_revenue = 0
        total_rooms = 0
        total_occupied = 0
        room_type_breakdown = {}
        
        for item in items:
            room_type = room_type_dict[item.room_type_id]
            inventory = room_type.inventory_count
            occupancy = item.forecasted_occupancy
            occupied_rooms = round(inventory * occupancy)
            revenue = occupied_rooms * item.final_price
            
            total_revenue += revenue
            total_rooms += inventory
            total_occupied += occupied_rooms
            
            # Add to room type breakdown
            if item.room_type_id not in room_type_breakdown:
                room_type_breakdown[item.room_type_id] = {
                    "room_type_id": item.room_type_id,
                    "room_type_name": room_type.name,
                    "revenue": 0,
                    "rooms": 0,
                    "occupied": 0,
                    "occupancy_rate": 0
                }
            
            room_type_breakdown[item.room_type_id]["revenue"] += revenue
            room_type_breakdown[item.room_type_id]["rooms"] += inventory
            room_type_breakdown[item.room_type_id]["occupied"] += occupied_rooms
        
        # Calculate occupancy rates
        overall_occupancy = total_occupied / total_rooms if total_rooms > 0 else 0
        
        for rt_id in room_type_breakdown:
            rt_data = room_type_breakdown[rt_id]
            rt_data["occupancy_rate"] = rt_data["occupied"] / rt_data["rooms"] if rt_data["rooms"] > 0 else 0
        
        # Add to analytics data
        analytics_data.append({
            "date": date_key.isoformat(),
            "total_revenue": round(total_revenue, 2),
            "total_rooms": total_rooms,
            "total_occupied": total_occupied,
            "occupancy_rate": round(overall_occupancy, 4),
            "room_types": list(room_type_breakdown.values())
        })
    
    # Sort by date
    analytics_data.sort(key=lambda x: x["date"])
    
    return {
        "hotel_id": hotel_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "group_by": group_by,
        "analytics": analytics_data
    }


@router.get("/occupancy/{hotel_id}")
def get_occupancy_analytics(
    hotel_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    room_type_id: Optional[int] = None,
    group_by: str = "day",  # day, week, month
    db: Session = Depends(get_db)
):
    """
    Get occupancy analytics for a hotel.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().date()
    
    if not start_date:
        # Default to 30 days before end_date
        start_date = end_date - timedelta(days=30)
    
    # Build query for room types
    room_types_query = db.query(RoomType).filter(RoomType.hotel_id == hotel_id)
    if room_type_id:
        room_types_query = room_types_query.filter(RoomType.id == room_type_id)
    
    room_types = room_types_query.all()
    if not room_types:
        raise HTTPException(
            status_code=404,
            detail=f"No room types found for hotel ID {hotel_id}"
        )
    
    # Get room type IDs
    room_type_ids = [rt.id for rt in room_types]
    
    # Build query for pricing data
    query = db.query(
        RoomPricing.date,
        RoomPricing.room_type_id,
        RoomPricing.forecasted_occupancy
    ).filter(
        RoomPricing.room_type_id.in_(room_type_ids),
        RoomPricing.date >= start_date,
        RoomPricing.date <= end_date
    )
    
    pricing_data = query.all()
    
    # Process data for analytics
    analytics_data = []
    room_type_dict = {rt.id: rt for rt in room_types}
    
    # Group data by date
    date_grouped_data = {}
    for item in pricing_data:
        date_key = item.date
        
        # Adjust key based on group_by parameter
        if group_by == "week":
            # Get the Monday of the week
            date_key = item.date - timedelta(days=item.date.weekday())
        elif group_by == "month":
            # Get the first day of the month
            date_key = date(item.date.year, item.date.month, 1)
        
        if date_key not in date_grouped_data:
            date_grouped_data[date_key] = []
        
        date_grouped_data[date_key].append(item)
    
    # Calculate analytics for each group
    for date_key, items in date_grouped_data.items():
        total_rooms = 0
        total_occupied = 0
        room_type_breakdown = {}
        
        for item in items:
            room_type = room_type_dict[item.room_type_id]
            inventory = room_type.inventory_count
            occupancy = item.forecasted_occupancy
            occupied_rooms = round(inventory * occupancy)
            
            total_rooms += inventory
            total_occupied += occupied_rooms
            
            # Add to room type breakdown
            if item.room_type_id not in room_type_breakdown:
                room_type_breakdown[item.room_type_id] = {
                    "room_type_id": item.room_type_id,
                    "room_type_name": room_type.name,
                    "rooms": 0,
                    "occupied": 0,
                    "occupancy_rate": 0
                }
            
            room_type_breakdown[item.room_type_id]["rooms"] += inventory
            room_type_breakdown[item.room_type_id]["occupied"] += occupied_rooms
        
        # Calculate occupancy rates
        overall_occupancy = total_occupied / total_rooms if total_rooms > 0 else 0
        
        for rt_id in room_type_breakdown:
            rt_data = room_type_breakdown[rt_id]
            rt_data["occupancy_rate"] = rt_data["occupied"] / rt_data["rooms"] if rt_data["rooms"] > 0 else 0
        
        # Add to analytics data
        analytics_data.append({
            "date": date_key.isoformat(),
            "total_rooms": total_rooms,
            "total_occupied": total_occupied,
            "occupancy_rate": round(overall_occupancy, 4),
            "room_types": list(room_type_breakdown.values())
        })
    
    # Sort by date
    analytics_data.sort(key=lambda x: x["date"])
    
    return {
        "hotel_id": hotel_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "group_by": group_by,
        "analytics": analytics_data
    }


@router.get("/contribution-margin/{hotel_id}")
def get_contribution_margin_analytics(
    hotel_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    room_type_id: Optional[int] = None,
    group_by: str = "day",  # day, week, month
    db: Session = Depends(get_db)
):
    """
    Get contribution margin analytics for a hotel.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().date()
    
    if not start_date:
        # Default to 30 days before end_date
        start_date = end_date - timedelta(days=30)
    
    # Build query for room types
    room_types_query = db.query(RoomType).filter(RoomType.hotel_id == hotel_id)
    if room_type_id:
        room_types_query = room_types_query.filter(RoomType.id == room_type_id)
    
    room_types = room_types_query.all()
    if not room_types:
        raise HTTPException(
            status_code=404,
            detail=f"No room types found for hotel ID {hotel_id}"
        )
    
    # Get room type IDs
    room_type_ids = [rt.id for rt in room_types]
    
    # Build query for pricing data
    query = db.query(
        RoomPricing.date,
        RoomPricing.room_type_id,
        RoomPricing.final_price,
        RoomPricing.forecasted_occupancy
    ).filter(
        RoomPricing.room_type_id.in_(room_type_ids),
        RoomPricing.date >= start_date,
        RoomPricing.date <= end_date
    )
    
    pricing_data = query.all()
    
    # Process data for analytics
    analytics_data = []
    room_type_dict = {rt.id: rt for rt in room_types}
    
    # Group data by date
    date_grouped_data = {}
    for item in pricing_data:
        date_key = item.date
        
        # Adjust key based on group_by parameter
        if group_by == "week":
            # Get the Monday of the week
            date_key = item.date - timedelta(days=item.date.weekday())
        elif group_by == "month":
            # Get the first day of the month
            date_key = date(item.date.year, item.date.month, 1)
        
        if date_key not in date_grouped_data:
            date_grouped_data[date_key] = []
        
        date_grouped_data[date_key].append(item)
    
    # Calculate analytics for each group
    for date_key, items in date_grouped_data.items():
        total_revenue = 0
        total_variable_cost = 0
        total_contribution = 0
        total_rooms = 0
        total_occupied = 0
        room_type_breakdown = {}
        
        for item in items:
            room_type = room_type_dict[item.room_type_id]
            inventory = room_type.inventory_count
            occupancy = item.forecasted_occupancy
            occupied_rooms = round(inventory * occupancy)
            revenue = occupied_rooms * item.final_price
            variable_cost = occupied_rooms * room_type.variable_cost
            contribution = revenue - variable_cost
            
            total_revenue += revenue
            total_variable_cost += variable_cost
            total_contribution += contribution
            total_rooms += inventory
            total_occupied += occupied_rooms
            
            # Add to room type breakdown
            if item.room_type_id not in room_type_breakdown:
                room_type_breakdown[item.room_type_id] = {
                    "room_type_id": item.room_type_id,
                    "room_type_name": room_type.name,
                    "revenue": 0,
                    "variable_cost": 0,
                    "contribution": 0,
                    "contribution_margin": 0,
                    "rooms": 0,
                    "occupied": 0
                }
            
            room_type_breakdown[item.room_type_id]["revenue"] += revenue
            room_type_breakdown[item.room_type_id]["variable_cost"] += variable_cost
            room_type_breakdown[item.room_type_id]["contribution"] += contribution
            room_type_breakdown[item.room_type_id]["rooms"] += inventory
            room_type_breakdown[item.room_type_id]["occupied"] += occupied_rooms
        
        # Calculate contribution margins
        overall_contribution_margin = total_contribution / total_revenue if total_revenue > 0 else 0
        
        for rt_id in room_type_breakdown:
            rt_data = room_type_breakdown[rt_id]
            rt_data["contribution_margin"] = rt_data["contribution"] / rt_data["revenue"] if rt_data["revenue"] > 0 else 0
        
        # Add to analytics data
        analytics_data.append({
            "date": date_key.isoformat(),
            "total_revenue": round(total_revenue, 2),
            "total_variable_cost": round(total_variable_cost, 2),
            "total_contribution": round(total_contribution, 2),
            "contribution_margin": round(overall_contribution_margin, 4),
            "total_rooms": total_rooms,
            "total_occupied": total_occupied,
            "room_types": list(room_type_breakdown.values())
        })
    
    # Sort by date
    analytics_data.sort(key=lambda x: x["date"])
    
    return {
        "hotel_id": hotel_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "group_by": group_by,
        "analytics": analytics_data
    }


@router.get("/pricing-performance/{hotel_id}")
def get_pricing_performance_analytics(
    hotel_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    room_type_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get pricing performance analytics for a hotel, comparing suggested vs. final prices.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().date()
    
    if not start_date:
        # Default to 30 days before end_date
        start_date = end_date - timedelta(days=30)
    
    # Build query for room types
    room_types_query = db.query(RoomType).filter(RoomType.hotel_id == hotel_id)
    if room_type_id:
        room_types_query = room_types_query.filter(RoomType.id == room_type_id)
    
    room_types = room_types_query.all()
    if not room_types:
        raise HTTPException(
            status_code=404,
            detail=f"No room types found for hotel ID {hotel_id}"
        )
    
    # Get room type IDs
    room_type_ids = [rt.id for rt in room_types]
    
    # Build query for pricing data
    query = db.query(
        RoomPricing.date,
        RoomPricing.room_type_id,
        RoomPricing.suggested_price,
        RoomPricing.final_price,
        RoomPricing.is_override,
        RoomPricing.forecasted_occupancy
    ).filter(
        RoomPricing.room_type_id.in_(room_type_ids),
        RoomPricing.date >= start_date,
        RoomPricing.date <= end_date
    )
    
    pricing_data = query.all()
    
    # Process data for analytics
    analytics_data = []
    room_type_dict = {rt.id: rt for rt in room_types}
    
    # Group data by room type
    room_type_grouped_data = {}
    for item in pricing_data:
        if item.room_type_id not in room_type_grouped_data:
            room_type_grouped_data[item.room_type_id] = []
        
        room_type_grouped_data[item.room_type_id].append(item)
    
    # Calculate analytics for each room type
    for rt_id, items in room_type_grouped_data.items():
        room_type = room_type_dict[rt_id]
        
        total_suggested_revenue = 0
        total_final_revenue = 0
        total_rooms = 0
        total_occupied = 0
        override_count = 0
        daily_data = []
        
        for item in items:
            inventory = room_type.inventory_count
            occupancy = item.forecasted_occupancy
            occupied_rooms = round(inventory * occupancy)
            
            suggested_revenue = occupied_rooms * item.suggested_price
            final_revenue = occupied_rooms * item.final_price
            
            total_suggested_revenue += suggested_revenue
            total_final_revenue += final_revenue
            total_rooms += inventory
            total_occupied += occupied_rooms
            
            if item.is_override:
                override_count += 1
            
            # Add daily data
            daily_data.append({
                "date": item.date.isoformat(),
                "suggested_price": round(item.suggested_price, 2),
                "final_price": round(item.final_price, 2),
                "is_override": item.is_override,
                "occupancy": round(occupancy, 4),
                "occupied_rooms": occupied_rooms,
                "suggested_revenue": round(suggested_revenue, 2),
                "final_revenue": round(final_revenue, 2),
                "revenue_difference": round(final_revenue - suggested_revenue, 2),
                "revenue_difference_percentage": round((final_revenue - suggested_revenue) / suggested_revenue * 100 if suggested_revenue > 0 else 0, 2)
            })
        
        # Calculate overall metrics
        revenue_difference = total_final_revenue - total_suggested_revenue
        revenue_difference_percentage = (revenue_difference / total_suggested_revenue * 100) if total_suggested_revenue > 0 else 0
        override_percentage = (override_count / len(items) * 100) if items else 0
        
        # Sort daily data by date
        daily_data.sort(key=lambda x: x["date"])
        
        # Add to analytics data
        analytics_data.append({
            "room_type_id": rt_id,
            "room_type_name": room_type.name,
            "total_suggested_revenue": round(total_suggested_revenue, 2),
            "total_final_revenue": round(total_final_revenue, 2),
            "revenue_difference": round(revenue_difference, 2),
            "revenue_difference_percentage": round(revenue_difference_percentage, 2),
            "total_days": len(items),
            "override_count": override_count,
            "override_percentage": round(override_percentage, 2),
            "daily_data": daily_data
        })
    
    return {
        "hotel_id": hotel_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "analytics": analytics_data
    }


@router.get("/export/{hotel_id}")
def export_analytics_data(
    hotel_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    data_type: str = "revenue",  # revenue, occupancy, contribution-margin, pricing
    room_type_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Export analytics data for a hotel in a format suitable for CSV export or BI tools.
    """
    # Check if hotel exists
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(
            status_code=404,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().date()
    
    if not start_date:
        # Default to 30 days before end_date
        start_date = end_date - timedelta(days=30)
    
    # Build query for room types
    room_types_query = db.query(RoomType).filter(RoomType.hotel_id == hotel_id)
    if room_type_id:
        room_types_query = room_types_query.filter(RoomType.id == room_type_id)
    
    room_types = room_types_query.all()
    if not room_types:
        raise HTTPException(
            status_code=404,
            detail=f"No room types found for hotel ID {hotel_id}"
        )
    
    # Get room type IDs
    room_type_ids = [rt.id for rt in room_types]
    room_type_dict = {rt.id: rt for rt in room_types}
    
    # Build query for pricing data
    query = db.query(
        RoomPricing.date,
        RoomPricing.room_type_id,
        RoomPricing.suggested_price,
        RoomPricing.final_price,
        RoomPricing.is_override,
        RoomPricing.forecasted_demand,
        RoomPricing.forecasted_occupancy
    ).filter(
        RoomPricing.room_type_id.in_(room_type_ids),
        RoomPricing.date >= start_date,
        RoomPricing.date <= end_date
    ).order_by(RoomPricing.date, RoomPricing.room_type_id)
    
    pricing_data = query.all()
    
    # Prepare export data
    export_data = []
    
    for item in pricing_data:
        room_type = room_type_dict[item.room_type_id]
        inventory = room_type.inventory_count
        occupancy = item.forecasted_occupancy
        occupied_rooms = round(inventory * occupancy)
        revenue = occupied_rooms * item.final_price
        variable_cost = occupied_rooms * room_type.variable_cost
        contribution = revenue - variable_cost
        contribution_margin = contribution / revenue if revenue > 0 else 0
        
        export_item = {
            "date": item.date.isoformat(),
            "room_type_id": item.room_type_id,
            "room_type_name": room_type.name,
            "base_price": room_type.base_price,
            "variable_cost": room_type.variable_cost,
            "inventory": inventory,
            "suggested_price": item.suggested_price,
            "final_price": item.final_price,
            "is_override": item.is_override,
            "forecasted_demand": item.forecasted_demand,
            "forecasted_occupancy": occupancy,
            "occupied_rooms": occupied_rooms,
            "revenue": revenue,
            "total_variable_cost": variable_cost,
            "contribution": contribution,
            "contribution_margin": contribution_margin
        }
        
        export_data.append(export_item)
    
    return {
        "hotel_id": hotel_id,
        "hotel_name": hotel.name,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "data_type": data_type,
        "export_data": export_data
    }
