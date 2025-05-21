from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Hotel(Base, TimestampMixin):
    """Hotel model representing a property in the system."""
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=True)
    currency = Column(String(3), nullable=False, default="USD")
    timezone = Column(String(50), nullable=False, default="UTC")
    logo_url = Column(String(255), nullable=True)
    primary_color = Column(String(7), nullable=True)  # Hex color code
    secondary_color = Column(String(7), nullable=True)  # Hex color code
    is_active = Column(Boolean, default=True)
    
    # Fixed costs
    monthly_fixed_costs = Column(Float, nullable=False, default=0.0)
    
    # Relationships
    rooms = relationship("RoomType", back_populates="hotel", cascade="all, delete-orphan")
    pricing_rules = relationship("PricingRule", back_populates="hotel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Hotel {self.name}>"


class RoomType(Base, TimestampMixin):
    """Room type model representing a category of rooms in a hotel."""
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    base_price = Column(Float, nullable=False)  # Standard/rack rate
    variable_cost = Column(Float, nullable=False)  # Cost per occupied room
    inventory_count = Column(Integer, nullable=False)  # Number of rooms of this type
    max_occupancy = Column(Integer, nullable=False, default=2)
    amenities = Column(Text, nullable=True)  # JSON string of amenities
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    hotel = relationship("Hotel", back_populates="rooms")
    pricing_history = relationship("RoomPricing", back_populates="room_type", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<RoomType {self.name} at {self.hotel.name}>"


class RoomPricing(Base, TimestampMixin):
    """Daily pricing for a specific room type."""
    __tablename__ = "room_pricing"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    suggested_price = Column(Float, nullable=False)
    final_price = Column(Float, nullable=False)  # After manual override if any
    is_override = Column(Boolean, default=False)
    override_notes = Column(Text, nullable=True)
    forecasted_demand = Column(Float, nullable=True)  # 0-1 probability
    forecasted_occupancy = Column(Float, nullable=True)  # 0-1 probability
    
    # Relationships
    room_type = relationship("RoomType", back_populates="pricing_history")
    
    def __repr__(self):
        return f"<RoomPricing for {self.room_type.name} on {self.date}>"


class PricingRule(Base, TimestampMixin):
    """Business rules for dynamic pricing."""
    __tablename__ = "pricing_rules"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    min_price_multiplier = Column(Float, nullable=False, default=0.5)  # Minimum price as % of base price
    max_price_multiplier = Column(Float, nullable=False, default=2.0)  # Maximum price as % of base price
    low_demand_threshold = Column(Float, nullable=False, default=0.3)  # 0-1 probability
    high_demand_threshold = Column(Float, nullable=False, default=0.7)  # 0-1 probability
    is_active = Column(Boolean, default=True)
    
    # Relationships
    hotel = relationship("Hotel", back_populates="pricing_rules")
    
    def __repr__(self):
        return f"<PricingRule {self.name} for {self.hotel.name}>"
