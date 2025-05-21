import logging
from sqlalchemy.orm import Session

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.hotel import Hotel, RoomType, PricingRule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize database with sample data."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(Hotel).count() > 0:
        logger.info("Database already contains data, skipping initialization")
        db.close()
        return
    
    try:
        # Create sample hotels
        logger.info("Creating sample hotels")
        
        # Grand Hotel
        grand_hotel = Hotel(
            name="Grand Hotel",
            address="123 Main Street",
            city="New York",
            state="NY",
            country="USA",
            zip_code="10001",
            currency="USD",
            timezone="America/New_York",
            logo_url="https://example.com/grand_hotel_logo.png",
            primary_color="#1E3A8A",
            secondary_color="#BFDBFE",
            monthly_fixed_costs=85000.00,
            is_active=True
        )
        db.add(grand_hotel)
        db.flush()  # Flush to get the ID
        
        # City Center Hotel
        city_center_hotel = Hotel(
            name="City Center Hotel",
            address="456 Park Avenue",
            city="Chicago",
            state="IL",
            country="USA",
            zip_code="60601",
            currency="USD",
            timezone="America/Chicago",
            logo_url="https://example.com/city_center_logo.png",
            primary_color="#047857",
            secondary_color="#D1FAE5",
            monthly_fixed_costs=65000.00,
            is_active=True
        )
        db.add(city_center_hotel)
        db.flush()
        
        # Business Hotel
        business_hotel = Hotel(
            name="Business Hotel",
            address="789 Market Street",
            city="San Francisco",
            state="CA",
            country="USA",
            zip_code="94103",
            currency="USD",
            timezone="America/Los_Angeles",
            logo_url="https://example.com/business_hotel_logo.png",
            primary_color="#7C3AED",
            secondary_color="#EDE9FE",
            monthly_fixed_costs=75000.00,
            is_active=True
        )
        db.add(business_hotel)
        db.flush()
        
        # Create room types for Grand Hotel
        logger.info("Creating room types for Grand Hotel")
        
        standard_room_grand = RoomType(
            hotel_id=grand_hotel.id,
            name="Standard Room",
            description="Comfortable room with a queen-size bed, suitable for up to 2 guests.",
            base_price=199.00,
            variable_cost=45.00,
            inventory_count=40,
            max_occupancy=2,
            amenities="Wi-Fi, TV, Mini-bar, Coffee maker",
            image_url="https://example.com/grand_standard_room.jpg",
            is_active=True
        )
        db.add(standard_room_grand)
        
        deluxe_room_grand = RoomType(
            hotel_id=grand_hotel.id,
            name="Deluxe Room",
            description="Spacious room with a king-size bed, suitable for up to 2 guests.",
            base_price=299.00,
            variable_cost=65.00,
            inventory_count=30,
            max_occupancy=2,
            amenities="Wi-Fi, TV, Mini-bar, Coffee maker, Bathrobe, Slippers",
            image_url="https://example.com/grand_deluxe_room.jpg",
            is_active=True
        )
        db.add(deluxe_room_grand)
        
        suite_grand = RoomType(
            hotel_id=grand_hotel.id,
            name="Executive Suite",
            description="Luxurious suite with a king-size bed and separate living area.",
            base_price=499.00,
            variable_cost=95.00,
            inventory_count=15,
            max_occupancy=3,
            amenities="Wi-Fi, TV, Mini-bar, Coffee maker, Bathrobe, Slippers, Jacuzzi",
            image_url="https://example.com/grand_suite.jpg",
            is_active=True
        )
        db.add(suite_grand)
        
        # Create room types for City Center Hotel
        logger.info("Creating room types for City Center Hotel")
        
        standard_room_city = RoomType(
            hotel_id=city_center_hotel.id,
            name="Standard Room",
            description="Comfortable room with a queen-size bed.",
            base_price=149.00,
            variable_cost=35.00,
            inventory_count=50,
            max_occupancy=2,
            amenities="Wi-Fi, TV, Coffee maker",
            image_url="https://example.com/city_standard_room.jpg",
            is_active=True
        )
        db.add(standard_room_city)
        
        deluxe_room_city = RoomType(
            hotel_id=city_center_hotel.id,
            name="Deluxe Room",
            description="Spacious room with a king-size bed.",
            base_price=229.00,
            variable_cost=55.00,
            inventory_count=35,
            max_occupancy=2,
            amenities="Wi-Fi, TV, Mini-bar, Coffee maker, Bathrobe",
            image_url="https://example.com/city_deluxe_room.jpg",
            is_active=True
        )
        db.add(deluxe_room_city)
        
        # Create room types for Business Hotel
        logger.info("Creating room types for Business Hotel")
        
        standard_room_business = RoomType(
            hotel_id=business_hotel.id,
            name="Standard Room",
            description="Practical room with a queen-size bed and work desk.",
            base_price=169.00,
            variable_cost=40.00,
            inventory_count=45,
            max_occupancy=2,
            amenities="Wi-Fi, TV, Coffee maker, Work desk",
            image_url="https://example.com/business_standard_room.jpg",
            is_active=True
        )
        db.add(standard_room_business)
        
        executive_room_business = RoomType(
            hotel_id=business_hotel.id,
            name="Executive Room",
            description="Spacious room with a king-size bed and large work area.",
            base_price=249.00,
            variable_cost=60.00,
            inventory_count=30,
            max_occupancy=2,
            amenities="Wi-Fi, TV, Mini-bar, Coffee maker, Work desk, Printer",
            image_url="https://example.com/business_executive_room.jpg",
            is_active=True
        )
        db.add(executive_room_business)
        
        # Create pricing rules
        logger.info("Creating pricing rules")
        
        # Grand Hotel pricing rule
        grand_hotel_rule = PricingRule(
            hotel_id=grand_hotel.id,
            name="Standard Dynamic Pricing",
            description="Standard dynamic pricing rule with moderate price flexibility",
            min_price_multiplier=0.6,
            max_price_multiplier=1.8,
            low_demand_threshold=0.4,
            high_demand_threshold=0.8,
            is_active=True
        )
        db.add(grand_hotel_rule)
        
        # City Center Hotel pricing rule
        city_center_rule = PricingRule(
            hotel_id=city_center_hotel.id,
            name="Aggressive Dynamic Pricing",
            description="Aggressive pricing strategy with higher price flexibility",
            min_price_multiplier=0.5,
            max_price_multiplier=2.0,
            low_demand_threshold=0.3,
            high_demand_threshold=0.7,
            is_active=True
        )
        db.add(city_center_rule)
        
        # Business Hotel pricing rule
        business_hotel_rule = PricingRule(
            hotel_id=business_hotel.id,
            name="Conservative Dynamic Pricing",
            description="Conservative pricing strategy with lower price flexibility",
            min_price_multiplier=0.7,
            max_price_multiplier=1.5,
            low_demand_threshold=0.5,
            high_demand_threshold=0.8,
            is_active=True
        )
        db.add(business_hotel_rule)
        
        # Commit all changes
        db.commit()
        logger.info("Sample data created successfully")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")
