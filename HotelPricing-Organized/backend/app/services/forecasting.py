import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from prophet import Prophet
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session

from app.models.hotel import Hotel, RoomType, RoomPricing
from app.core.config import settings


class DemandForecaster:
    """
    Demand forecasting service that predicts future hotel room demand
    using historical booking data, seasonality, and external factors.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.prophet_model = None
        self.xgb_model = None
        self.scaler = StandardScaler()
    
    def train_prophet_model(self, hotel_id: int, room_type_id: Optional[int] = None) -> None:
        """
        Train a Prophet model for time series forecasting based on historical data.
        
        Args:
            hotel_id: ID of the hotel
            room_type_id: Optional ID of specific room type, or None for all rooms
        """
        # In a real implementation, this would fetch historical booking data
        # For now, we'll simulate with a basic implementation
        
        # Create a dataframe with historical data (past 2 years)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=730)  # 2 years of data
        
        # Generate dates
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Simulate occupancy data with seasonality
        # Higher in summer (Jun-Aug) and weekends, lower in winter
        occupancy = []
        for date in dates:
            # Base occupancy
            base = 0.6
            
            # Seasonal component (higher in summer)
            month = date.month
            if 6 <= month <= 8:  # Summer
                seasonal = 0.2
            elif 11 <= month <= 2:  # Winter
                seasonal = -0.15
            else:  # Spring/Fall
                seasonal = 0.05
                
            # Day of week component (higher on weekends)
            day_of_week = date.weekday()
            if day_of_week >= 5:  # Weekend
                dow = 0.15
            else:
                dow = 0
                
            # Add some noise
            noise = np.random.normal(0, 0.05)
            
            # Calculate final occupancy (capped between 0 and 1)
            occ = min(max(base + seasonal + dow + noise, 0), 1)
            occupancy.append(occ)
        
        # Create the dataframe
        df = pd.DataFrame({
            'ds': dates,
            'y': occupancy
        })
        
        # Train Prophet model
        self.prophet_model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='multiplicative'
        )
        self.prophet_model.fit(df)
    
    def train_xgb_model(self, hotel_id: int, room_type_id: Optional[int] = None) -> None:
        """
        Train an XGBoost model for demand forecasting with additional features.
        
        Args:
            hotel_id: ID of the hotel
            room_type_id: Optional ID of specific room type, or None for all rooms
        """
        # In a real implementation, this would prepare a feature-rich dataset
        # For now, we'll implement a simplified version
        
        # Create a dataframe with historical data (past 2 years)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=730)  # 2 years of data
        
        # Generate dates
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Create features and target
        data = []
        for date in dates:
            # Features
            month = date.month
            day_of_week = date.weekday()
            is_weekend = 1 if day_of_week >= 5 else 0
            is_summer = 1 if 6 <= month <= 8 else 0
            is_winter = 1 if month <= 2 or month == 12 else 0
            
            # Simulate price (higher in high season)
            base_price = 100
            if is_summer:
                price = base_price * (1.2 + np.random.normal(0, 0.1))
            elif is_winter:
                price = base_price * (0.8 + np.random.normal(0, 0.1))
            else:
                price = base_price * (1.0 + np.random.normal(0, 0.1))
                
            # Simulate occupancy based on features
            base = 0.6
            seasonal = 0.2 if is_summer else (-0.15 if is_winter else 0.05)
            dow = 0.15 if is_weekend else 0
            price_effect = -0.1 if price > base_price * 1.1 else 0.1 if price < base_price * 0.9 else 0
            noise = np.random.normal(0, 0.05)
            
            occupancy = min(max(base + seasonal + dow + price_effect + noise, 0), 1)
            
            # Add to data
            data.append({
                'date': date,
                'month': month,
                'day_of_week': day_of_week,
                'is_weekend': is_weekend,
                'is_summer': is_summer,
                'is_winter': is_winter,
                'price': price,
                'occupancy': occupancy
            })
        
        # Create dataframe
        df = pd.DataFrame(data)
        
        # Prepare features and target
        X = df[['month', 'day_of_week', 'is_weekend', 'is_summer', 'is_winter', 'price']]
        y = df['occupancy']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train XGBoost model
        self.xgb_model = XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='reg:squarederror'
        )
        self.xgb_model.fit(X_scaled, y)
    
    def forecast_demand(
        self, 
        hotel_id: int, 
        room_type_id: int, 
        start_date: datetime, 
        days: int = 90
    ) -> List[Dict[str, Any]]:
        """
        Generate demand forecast for a specific room type over a future period.
        
        Args:
            hotel_id: ID of the hotel
            room_type_id: ID of the room type
            start_date: Start date for the forecast
            days: Number of days to forecast
            
        Returns:
            List of daily forecasts with date and demand probability
        """
        # Ensure models are trained
        if self.prophet_model is None:
            self.train_prophet_model(hotel_id, room_type_id)
        
        if self.xgb_model is None:
            self.train_xgb_model(hotel_id, room_type_id)
        
        # Generate future dates for Prophet
        future_dates = pd.DataFrame({
            'ds': pd.date_range(start=start_date, periods=days, freq='D')
        })
        
        # Get Prophet forecast
        prophet_forecast = self.prophet_model.predict(future_dates)
        
        # Prepare data for XGBoost
        xgb_data = []
        for date in future_dates['ds']:
            # Features
            month = date.month
            day_of_week = date.weekday()
            is_weekend = 1 if day_of_week >= 5 else 0
            is_summer = 1 if 6 <= month <= 8 else 0
            is_winter = 1 if month <= 2 or month == 12 else 0
            
            # Get room type base price
            room_type = self.db.query(RoomType).filter(RoomType.id == room_type_id).first()
            base_price = room_type.base_price if room_type else 100
            
            # Simulate price based on season
            if is_summer:
                price = base_price * 1.2
            elif is_winter:
                price = base_price * 0.8
            else:
                price = base_price
            
            xgb_data.append({
                'month': month,
                'day_of_week': day_of_week,
                'is_weekend': is_weekend,
                'is_summer': is_summer,
                'is_winter': is_winter,
                'price': price
            })
        
        # Create dataframe for XGBoost
        xgb_df = pd.DataFrame(xgb_data)
        
        # Scale features
        X_xgb_scaled = self.scaler.transform(xgb_df)
        
        # Get XGBoost forecast
        xgb_forecast = self.xgb_model.predict(X_xgb_scaled)
        
        # Combine forecasts (simple average)
        combined_forecast = []
        for i, date in enumerate(future_dates['ds']):
            # Get Prophet forecast (ensure it's between 0 and 1)
            prophet_value = min(max(prophet_forecast['yhat'].iloc[i], 0), 1)
            
            # Get XGBoost forecast
            xgb_value = xgb_forecast[i]
            
            # Combine (simple average)
            combined_value = (prophet_value + xgb_value) / 2
            
            combined_forecast.append({
                'date': date.date().isoformat(),
                'demand_probability': combined_value,
                'prophet_forecast': prophet_value,
                'xgb_forecast': xgb_value
            })
        
        return combined_forecast
    
    def simulate_price_elasticity(
        self, 
        hotel_id: int, 
        room_type_id: int, 
        date: datetime, 
        price_range: List[float]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Simulate price elasticity by predicting demand at different price points.
        
        Args:
            hotel_id: ID of the hotel
            room_type_id: ID of the room type
            date: Date to simulate for
            price_range: List of prices to simulate
            
        Returns:
            Dictionary with price elasticity data
        """
        # Ensure XGBoost model is trained
        if self.xgb_model is None:
            self.train_xgb_model(hotel_id, room_type_id)
        
        # Prepare data for different price points
        elasticity_data = []
        
        for price in price_range:
            # Features
            month = date.month
            day_of_week = date.weekday()
            is_weekend = 1 if day_of_week >= 5 else 0
            is_summer = 1 if 6 <= month <= 8 else 0
            is_winter = 1 if month <= 2 or month == 12 else 0
            
            # Create feature array
            features = np.array([[
                month, day_of_week, is_weekend, is_summer, is_winter, price
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict demand
            demand = self.xgb_model.predict(features_scaled)[0]
            
            # Get room type details
            room_type = self.db.query(RoomType).filter(RoomType.id == room_type_id).first()
            
            # Calculate contribution margin
            variable_cost = room_type.variable_cost if room_type else 30
            contribution_margin = price - variable_cost
            
            # Calculate expected revenue (demand * price * inventory)
            inventory = room_type.inventory_count if room_type else 10
            expected_revenue = demand * price * inventory
            
            # Calculate expected contribution (demand * contribution_margin * inventory)
            expected_contribution = demand * contribution_margin * inventory
            
            elasticity_data.append({
                'price': price,
                'demand_probability': demand,
                'contribution_margin': contribution_margin,
                'expected_revenue': expected_revenue,
                'expected_contribution': expected_contribution
            })
        
        return {
            'date': date.date().isoformat(),
            'elasticity': elasticity_data
        }
