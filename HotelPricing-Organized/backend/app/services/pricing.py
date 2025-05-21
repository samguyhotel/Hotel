from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from app.models.hotel import Hotel, RoomType, RoomPricing, PricingRule
from app.services.forecasting import DemandForecaster
from app.core.config import settings


class DynamicPricingEngine:
    """
    Dynamic pricing engine that determines optimal room prices based on
    demand forecasts and contribution margin logic.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.forecaster = DemandForecaster(db)
    
    def calculate_optimal_price(
        self,
        room_type_id: int,
        date: datetime,
        demand_probability: float,
        override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate the optimal price for a room based on demand and costs.
        
        Args:
            room_type_id: ID of the room type
            date: Date to calculate price for
            demand_probability: Forecasted demand probability (0-1)
            override: Optional manual override data
            
        Returns:
            Dictionary with pricing details
        """
        # Get room type details
        room_type = self.db.query(RoomType).filter(RoomType.id == room_type_id).first()
        if not room_type:
            raise ValueError(f"Room type with ID {room_type_id} not found")
        
        # Get hotel details
        hotel = self.db.query(Hotel).filter(Hotel.id == room_type.hotel_id).first()
        if not hotel:
            raise ValueError(f"Hotel with ID {room_type.hotel_id} not found")
        
        # Get pricing rules
        pricing_rule = self.db.query(PricingRule).filter(
            PricingRule.hotel_id == hotel.id,
            PricingRule.is_active == True
        ).first()
        
        if not pricing_rule:
            # Create default pricing rule if none exists
            pricing_rule = PricingRule(
                hotel_id=hotel.id,
                name="Default Rule",
                description="System-generated default rule",
                min_price_multiplier=0.5,
                max_price_multiplier=2.0,
                low_demand_threshold=0.3,
                high_demand_threshold=0.7,
                is_active=True
            )
        
        # Calculate price based on demand
        base_price = room_type.base_price
        variable_cost = room_type.variable_cost
        
        # Determine price multiplier based on demand
        if demand_probability <= pricing_rule.low_demand_threshold:
            # Low demand - discount prices
            # Linear scale from min_multiplier at 0 demand to 1.0 at low_threshold
            demand_ratio = demand_probability / pricing_rule.low_demand_threshold
            price_multiplier = pricing_rule.min_price_multiplier + (1 - pricing_rule.min_price_multiplier) * demand_ratio
        elif demand_probability >= pricing_rule.high_demand_threshold:
            # High demand - premium prices
            # Linear scale from 1.0 at high_threshold to max_multiplier at 1.0 demand
            demand_ratio = (demand_probability - pricing_rule.high_demand_threshold) / (1 - pricing_rule.high_demand_threshold)
            price_multiplier = 1.0 + (pricing_rule.max_price_multiplier - 1.0) * demand_ratio
        else:
            # Normal demand - standard pricing
            # Linear scale from 1.0 at low_threshold to 1.0 at high_threshold
            price_multiplier = 1.0
        
        # Calculate suggested price
        suggested_price = base_price * price_multiplier
        
        # Ensure price covers variable costs plus minimum contribution margin
        min_price = variable_cost + settings.MIN_CONTRIBUTION_MARGIN
        if suggested_price < min_price:
            suggested_price = min_price
        
        # Apply override if provided
        is_override = False
        override_notes = None
        final_price = suggested_price
        
        if override and 'price' in override:
            final_price = override['price']
            is_override = True
            override_notes = override.get('notes', 'Manual override')
        
        # Calculate contribution margin
        contribution_margin = final_price - variable_cost
        contribution_margin_percentage = (contribution_margin / final_price) * 100 if final_price > 0 else 0
        
        # Calculate expected revenue based on demand
        expected_occupancy = demand_probability
        inventory_count = room_type.inventory_count
        expected_bookings = expected_occupancy * inventory_count
        expected_revenue = expected_bookings * final_price
        expected_contribution = expected_bookings * contribution_margin
        
        return {
            'date': date.date().isoformat(),
            'room_type_id': room_type_id,
            'room_type_name': room_type.name,
            'base_price': base_price,
            'variable_cost': variable_cost,
            'demand_probability': demand_probability,
            'price_multiplier': price_multiplier,
            'suggested_price': round(suggested_price, 2),
            'final_price': round(final_price, 2),
            'is_override': is_override,
            'override_notes': override_notes,
            'contribution_margin': round(contribution_margin, 2),
            'contribution_margin_percentage': round(contribution_margin_percentage, 2),
            'expected_occupancy': round(expected_occupancy, 4),
            'expected_bookings': round(expected_bookings, 2),
            'expected_revenue': round(expected_revenue, 2),
            'expected_contribution': round(expected_contribution, 2)
        }
    
    def generate_pricing_recommendations(
        self,
        hotel_id: int,
        start_date: datetime,
        days: int = 30,
        room_type_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate pricing recommendations for all room types in a hotel.
        
        Args:
            hotel_id: ID of the hotel
            start_date: Start date for recommendations
            days: Number of days to generate recommendations for
            room_type_id: Optional specific room type ID
            
        Returns:
            Dictionary with pricing recommendations
        """
        # Get room types
        query = self.db.query(RoomType).filter(RoomType.hotel_id == hotel_id, RoomType.is_active == True)
        if room_type_id:
            query = query.filter(RoomType.id == room_type_id)
        
        room_types = query.all()
        if not room_types:
            raise ValueError(f"No active room types found for hotel ID {hotel_id}")
        
        # Generate recommendations for each room type
        recommendations = {}
        
        for room_type in room_types:
            # Get demand forecast
            demand_forecast = self.forecaster.forecast_demand(
                hotel_id=hotel_id,
                room_type_id=room_type.id,
                start_date=start_date,
                days=days
            )
            
            # Calculate optimal prices
            room_prices = []
            for day_forecast in demand_forecast:
                date = datetime.fromisoformat(day_forecast['date'])
                
                # Check if there's an existing override
                existing_pricing = self.db.query(RoomPricing).filter(
                    RoomPricing.room_type_id == room_type.id,
                    RoomPricing.date == date
                ).first()
                
                override = None
                if existing_pricing and existing_pricing.is_override:
                    override = {
                        'price': existing_pricing.final_price,
                        'notes': existing_pricing.override_notes
                    }
                
                # Calculate optimal price
                price_data = self.calculate_optimal_price(
                    room_type_id=room_type.id,
                    date=date,
                    demand_probability=day_forecast['demand_probability'],
                    override=override
                )
                
                room_prices.append(price_data)
            
            recommendations[room_type.id] = {
                'room_type_id': room_type.id,
                'room_type_name': room_type.name,
                'base_price': room_type.base_price,
                'variable_cost': room_type.variable_cost,
                'inventory_count': room_type.inventory_count,
                'prices': room_prices
            }
        
        return {
            'hotel_id': hotel_id,
            'start_date': start_date.date().isoformat(),
            'days': days,
            'generated_at': datetime.now().isoformat(),
            'recommendations': recommendations
        }
    
    def save_pricing_recommendations(
        self,
        hotel_id: int,
        recommendations: Dict[str, Any]
    ) -> None:
        """
        Save pricing recommendations to the database.
        
        Args:
            hotel_id: ID of the hotel
            recommendations: Pricing recommendations dictionary
        """
        for room_type_id, room_data in recommendations['recommendations'].items():
            for price_data in room_data['prices']:
                date = datetime.fromisoformat(price_data['date'])
                
                # Check if pricing record already exists
                existing = self.db.query(RoomPricing).filter(
                    RoomPricing.room_type_id == room_type_id,
                    RoomPricing.date == date
                ).first()
                
                if existing:
                    # Update existing record
                    existing.suggested_price = price_data['suggested_price']
                    if not existing.is_override:
                        existing.final_price = price_data['final_price']
                    existing.forecasted_demand = price_data['demand_probability']
                    existing.forecasted_occupancy = price_data['expected_occupancy']
                else:
                    # Create new record
                    new_pricing = RoomPricing(
                        room_type_id=room_type_id,
                        date=date,
                        suggested_price=price_data['suggested_price'],
                        final_price=price_data['final_price'],
                        is_override=price_data['is_override'],
                        override_notes=price_data['override_notes'],
                        forecasted_demand=price_data['demand_probability'],
                        forecasted_occupancy=price_data['expected_occupancy']
                    )
                    self.db.add(new_pricing)
        
        self.db.commit()
    
    def apply_price_override(
        self,
        room_type_id: int,
        date: datetime,
        price: float,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Apply a manual price override for a specific room on a specific date.
        
        Args:
            room_type_id: ID of the room type
            date: Date to override price for
            price: Override price
            notes: Optional notes explaining the override
            
        Returns:
            Updated pricing data
        """
        # Get existing pricing record
        pricing = self.db.query(RoomPricing).filter(
            RoomPricing.room_type_id == room_type_id,
            RoomPricing.date == date
        ).first()
        
        if pricing:
            # Update existing record
            pricing.final_price = price
            pricing.is_override = True
            pricing.override_notes = notes
        else:
            # Get room type for suggested price calculation
            room_type = self.db.query(RoomType).filter(RoomType.id == room_type_id).first()
            if not room_type:
                raise ValueError(f"Room type with ID {room_type_id} not found")
            
            # Create new record with default suggested price
            pricing = RoomPricing(
                room_type_id=room_type_id,
                date=date,
                suggested_price=room_type.base_price,  # Default to base price
                final_price=price,
                is_override=True,
                override_notes=notes,
                forecasted_demand=0.5,  # Default to 50% demand
                forecasted_occupancy=0.5  # Default to 50% occupancy
            )
            self.db.add(pricing)
        
        self.db.commit()
        
        # Get room type details for response
        room_type = self.db.query(RoomType).filter(RoomType.id == room_type_id).first()
        
        return {
            'room_type_id': room_type_id,
            'room_type_name': room_type.name if room_type else None,
            'date': date.date().isoformat(),
            'suggested_price': pricing.suggested_price,
            'final_price': pricing.final_price,
            'is_override': pricing.is_override,
            'override_notes': pricing.override_notes
        }
