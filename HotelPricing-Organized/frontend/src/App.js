import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Layout Components
import Dashboard from './components/layout/Dashboard';
import AuthLayout from './components/layout/AuthLayout';

// Pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import DashboardHome from './pages/dashboard/DashboardHome';
import HotelsList from './pages/hotels/HotelsList';
import HotelDetails from './pages/hotels/HotelDetails';
import RoomTypesList from './pages/rooms/RoomTypesList';
import RoomTypeDetails from './pages/rooms/RoomTypeDetails';
import DynamicPricing from './pages/pricing/DynamicPricing';
import PricingRules from './pages/pricing/PricingRules';
import DemandForecasting from './pages/forecasting/DemandForecasting';
import RevenueAnalytics from './pages/analytics/RevenueAnalytics';
import OccupancyAnalytics from './pages/analytics/OccupancyAnalytics';
import ContributionMarginAnalytics from './pages/analytics/ContributionMarginAnalytics';
import PricingPerformance from './pages/analytics/PricingPerformance';
import Settings from './pages/settings/Settings';
import UserProfile from './pages/settings/UserProfile';
import NotFound from './pages/NotFound';

// Theme Context
import { ThemeProvider } from './contexts/ThemeContext';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    const checkAuth = () => {
      const token = localStorage.getItem('token');
      setIsAuthenticated(!!token);
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <ThemeProvider>
      <ToastContainer position="top-right" autoClose={5000} />
      <Routes>
        {/* Auth Routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/register" element={<Register setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Route>

        {/* Protected Dashboard Routes */}
        <Route
          element={
            isAuthenticated ? (
              <Dashboard setIsAuthenticated={setIsAuthenticated} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        >
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardHome />} />
          
          {/* Hotels Management */}
          <Route path="/hotels" element={<HotelsList />} />
          <Route path="/hotels/:hotelId" element={<HotelDetails />} />
          
          {/* Room Types Management */}
          <Route path="/room-types" element={<RoomTypesList />} />
          <Route path="/room-types/:roomTypeId" element={<RoomTypeDetails />} />
          
          {/* Pricing Management */}
          <Route path="/pricing" element={<DynamicPricing />} />
          <Route path="/pricing/rules" element={<PricingRules />} />
          
          {/* Forecasting */}
          <Route path="/forecasting" element={<DemandForecasting />} />
          
          {/* Analytics */}
          <Route path="/analytics/revenue" element={<RevenueAnalytics />} />
          <Route path="/analytics/occupancy" element={<OccupancyAnalytics />} />
          <Route path="/analytics/contribution-margin" element={<ContributionMarginAnalytics />} />
          <Route path="/analytics/pricing-performance" element={<PricingPerformance />} />
          
          {/* Settings */}
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<UserProfile />} />
        </Route>

        {/* 404 Not Found */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;
