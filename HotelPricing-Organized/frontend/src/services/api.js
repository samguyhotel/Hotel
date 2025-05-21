import mockApi from './mockApi';

/**
 * API Service
 * 
 * This service handles all API calls to the backend.
 * For demonstration purposes, it uses the mockApi service.
 * In a production environment, this would make actual API calls.
 */

const api = {
  // Authentication
  login: async (email, password) => {
    return mockApi.login(email, password);
  },
  
  // Hotels
  getHotels: async () => {
    return mockApi.getHotels();
  },
  
  getHotelById: async (id) => {
    return mockApi.getHotelById(id);
  },
  
  // Room Types
  getRoomTypes: async (hotelId = null) => {
    return mockApi.getRoomTypes(hotelId);
  },
  
  getRoomTypeById: async (id) => {
    return mockApi.getRoomTypeById(id);
  },
  
  // Pricing
  getPricingRecommendations: async (hotelId, startDate = new Date(), days = 30, roomTypeId = null) => {
    return mockApi.getPricingRecommendations(hotelId, startDate, days, roomTypeId);
  },
  
  // Analytics
  getRevenueAnalytics: async (hotelId, startDate = new Date(), endDate = null, roomTypeId = null, groupBy = "day") => {
    return mockApi.getRevenueAnalytics(hotelId, startDate, endDate, roomTypeId, groupBy);
  },
  
  getOccupancyAnalytics: async (hotelId, startDate = new Date(), endDate = null, roomTypeId = null, groupBy = "day") => {
    return mockApi.getOccupancyAnalytics(hotelId, startDate, endDate, roomTypeId, groupBy);
  },
  
  getContributionMarginAnalytics: async (hotelId, startDate = new Date(), endDate = null, roomTypeId = null, groupBy = "day") => {
    return mockApi.getContributionMarginAnalytics(hotelId, startDate, endDate, roomTypeId, groupBy);
  },
  
  // Dashboard data
  getDashboardData: async () => {
    return mockApi.getDashboardData();
  }
};

export default api;
