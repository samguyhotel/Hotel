/**
 * Mock API Service
 * 
 * This service simulates backend API responses for demonstration purposes.
 * In a production environment, this would be replaced with actual API calls.
 */

// Mock data for hotels
const hotels = [
  {
    id: 1,
    name: "Grand Hotel",
    address: "123 Main Street",
    city: "New York",
    state: "NY",
    country: "USA",
    zip_code: "10001",
    currency: "USD",
    timezone: "America/New_York",
    logo_url: "https://via.placeholder.com/150",
    primary_color: "#1E3A8A",
    secondary_color: "#BFDBFE",
    monthly_fixed_costs: 85000.00,
    is_active: true,
    created_at: "2025-01-15T10:30:00Z",
    updated_at: "2025-05-10T14:20:00Z"
  },
  {
    id: 2,
    name: "City Center Hotel",
    address: "456 Park Avenue",
    city: "Chicago",
    state: "IL",
    country: "USA",
    zip_code: "60601",
    currency: "USD",
    timezone: "America/Chicago",
    logo_url: "https://via.placeholder.com/150",
    primary_color: "#047857",
    secondary_color: "#D1FAE5",
    monthly_fixed_costs: 65000.00,
    is_active: true,
    created_at: "2025-02-20T09:15:00Z",
    updated_at: "2025-05-12T11:45:00Z"
  },
  {
    id: 3,
    name: "Business Hotel",
    address: "789 Market Street",
    city: "San Francisco",
    state: "CA",
    country: "USA",
    zip_code: "94103",
    currency: "USD",
    timezone: "America/Los_Angeles",
    logo_url: "https://via.placeholder.com/150",
    primary_color: "#7C3AED",
    secondary_color: "#EDE9FE",
    monthly_fixed_costs: 75000.00,
    is_active: true,
    created_at: "2025-03-05T08:45:00Z",
    updated_at: "2025-05-15T16:30:00Z"
  }
];

// Mock data for room types
const roomTypes = [
  {
    id: 1,
    hotel_id: 1,
    name: "Standard Room",
    description: "Comfortable room with a queen-size bed, suitable for up to 2 guests.",
    base_price: 199.00,
    variable_cost: 45.00,
    inventory_count: 40,
    max_occupancy: 2,
    amenities: "Wi-Fi, TV, Mini-bar, Coffee maker",
    image_url: "https://via.placeholder.com/300x200",
    is_active: true,
    created_at: "2025-01-15T10:35:00Z",
    updated_at: "2025-05-10T14:25:00Z"
  },
  {
    id: 2,
    hotel_id: 1,
    name: "Deluxe Room",
    description: "Spacious room with a king-size bed, suitable for up to 2 guests.",
    base_price: 299.00,
    variable_cost: 65.00,
    inventory_count: 30,
    max_occupancy: 2,
    amenities: "Wi-Fi, TV, Mini-bar, Coffee maker, Bathrobe, Slippers",
    image_url: "https://via.placeholder.com/300x200",
    is_active: true,
    created_at: "2025-01-15T10:40:00Z",
    updated_at: "2025-05-10T14:30:00Z"
  },
  {
    id: 3,
    hotel_id: 1,
    name: "Executive Suite",
    description: "Luxurious suite with a king-size bed and separate living area.",
    base_price: 499.00,
    variable_cost: 95.00,
    inventory_count: 15,
    max_occupancy: 3,
    amenities: "Wi-Fi, TV, Mini-bar, Coffee maker, Bathrobe, Slippers, Jacuzzi",
    image_url: "https://via.placeholder.com/300x200",
    is_active: true,
    created_at: "2025-01-15T10:45:00Z",
    updated_at: "2025-05-10T14:35:00Z"
  },
  {
    id: 4,
    hotel_id: 2,
    name: "Standard Room",
    description: "Comfortable room with a queen-size bed.",
    base_price: 149.00,
    variable_cost: 35.00,
    inventory_count: 50,
    max_occupancy: 2,
    amenities: "Wi-Fi, TV, Coffee maker",
    image_url: "https://via.placeholder.com/300x200",
    is_active: true,
    created_at: "2025-02-20T09:20:00Z",
    updated_at: "2025-05-12T11:50:00Z"
  },
  {
    id: 5,
    hotel_id: 2,
    name: "Deluxe Room",
    description: "Spacious room with a king-size bed.",
    base_price: 229.00,
    variable_cost: 55.00,
    inventory_count: 35,
    max_occupancy: 2,
    amenities: "Wi-Fi, TV, Mini-bar, Coffee maker, Bathrobe",
    image_url: "https://via.placeholder.com/300x200",
    is_active: true,
    created_at: "2025-02-20T09:25:00Z",
    updated_at: "2025-05-12T11:55:00Z"
  },
  {
    id: 6,
    hotel_id: 3,
    name: "Standard Room",
    description: "Practical room with a queen-size bed and work desk.",
    base_price: 169.00,
    variable_cost: 40.00,
    inventory_count: 45,
    max_occupancy: 2,
    amenities: "Wi-Fi, TV, Coffee maker, Work desk",
    image_url: "https://via.placeholder.com/300x200",
    is_active: true,
    created_at: "2025-03-05T08:50:00Z",
    updated_at: "2025-05-15T16:35:00Z"
  },
  {
    id: 7,
    hotel_id: 3,
    name: "Executive Room",
    description: "Spacious room with a king-size bed and large work area.",
    base_price: 249.00,
    variable_cost: 60.00,
    inventory_count: 30,
    max_occupancy: 2,
    amenities: "Wi-Fi, TV, Mini-bar, Coffee maker, Work desk, Printer",
    image_url: "https://via.placeholder.com/300x200",
    is_active: true,
    created_at: "2025-03-05T08:55:00Z",
    updated_at: "2025-05-15T16:40:00Z"
  }
];

// Generate dynamic pricing data for the next 30 days
const generatePricingData = (roomTypeId, startDate = new Date()) => {
  const pricingData = [];
  const roomType = roomTypes.find(rt => rt.id === roomTypeId);
  
  if (!roomType) return [];
  
  for (let i = 0; i < 30; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);
    
    // Generate random demand between 0.2 and 0.9
    const demand = 0.2 + Math.random() * 0.7;
    
    // Calculate price multiplier based on demand
    let priceMultiplier;
    if (demand <= 0.3) {
      // Low demand - discount prices
      priceMultiplier = 0.6 + (demand / 0.3) * 0.4;
    } else if (demand >= 0.7) {
      // High demand - premium prices
      priceMultiplier = 1.0 + ((demand - 0.7) / 0.3) * 1.0;
    } else {
      // Normal demand - standard pricing
      priceMultiplier = 1.0;
    }
    
    // Calculate suggested price
    const suggestedPrice = Math.round(roomType.base_price * priceMultiplier * 100) / 100;
    
    // Randomly decide if there's an override (10% chance)
    const isOverride = Math.random() < 0.1;
    let finalPrice = suggestedPrice;
    let overrideNotes = null;
    
    if (isOverride) {
      // Random adjustment between -10% and +15%
      const adjustment = -0.1 + Math.random() * 0.25;
      finalPrice = Math.round(suggestedPrice * (1 + adjustment) * 100) / 100;
      overrideNotes = "Manual adjustment for market conditions";
    }
    
    // Calculate occupancy (correlated with demand but with some randomness)
    const occupancy = Math.min(0.95, Math.max(0.1, demand * (0.8 + Math.random() * 0.4)));
    
    // Calculate contribution margin
    const contributionMargin = finalPrice - roomType.variable_cost;
    const contributionMarginPercentage = (contributionMargin / finalPrice) * 100;
    
    // Calculate expected bookings and revenue
    const expectedBookings = Math.round(occupancy * roomType.inventory_count * 10) / 10;
    const expectedRevenue = expectedBookings * finalPrice;
    const expectedContribution = expectedBookings * contributionMargin;
    
    pricingData.push({
      date: date.toISOString().split('T')[0],
      room_type_id: roomTypeId,
      room_type_name: roomType.name,
      base_price: roomType.base_price,
      variable_cost: roomType.variable_cost,
      demand_probability: Math.round(demand * 100) / 100,
      price_multiplier: Math.round(priceMultiplier * 100) / 100,
      suggested_price: suggestedPrice,
      final_price: finalPrice,
      is_override: isOverride,
      override_notes: overrideNotes,
      contribution_margin: Math.round(contributionMargin * 100) / 100,
      contribution_margin_percentage: Math.round(contributionMarginPercentage * 100) / 100,
      expected_occupancy: Math.round(occupancy * 100) / 100,
      expected_bookings: expectedBookings,
      expected_revenue: Math.round(expectedRevenue * 100) / 100,
      expected_contribution: Math.round(expectedContribution * 100) / 100
    });
  }
  
  return pricingData;
};

// Generate revenue analytics data
const generateRevenueAnalytics = (hotelId, startDate = new Date(), days = 30, groupBy = "day") => {
  const analytics = [];
  const hotelRoomTypes = roomTypes.filter(rt => rt.hotel_id === hotelId);
  
  if (hotelRoomTypes.length === 0) return { analytics: [] };
  
  let currentDate = new Date(startDate);
  
  for (let i = 0; i < days; i++) {
    const date = new Date(currentDate);
    date.setDate(date.getDate() + i);
    
    // For weekly or monthly grouping, adjust the date
    let groupDate = new Date(date);
    if (groupBy === "week") {
      // Set to Monday of the week
      const day = groupDate.getDay();
      const diff = groupDate.getDate() - day + (day === 0 ? -6 : 1);
      groupDate = new Date(groupDate.setDate(diff));
    } else if (groupBy === "month") {
      // Set to first day of the month
      groupDate = new Date(groupDate.getFullYear(), groupDate.getMonth(), 1);
    }
    
    // Check if we already have an entry for this group date
    const existingIndex = analytics.findIndex(a => 
      new Date(a.date).toISOString().split('T')[0] === groupDate.toISOString().split('T')[0]
    );
    
    if (existingIndex >= 0) {
      // Update existing entry
      continue;
    }
    
    // Generate data for this date
    let totalRevenue = 0;
    let totalRooms = 0;
    let totalOccupied = 0;
    const roomTypeBreakdown = {};
    
    hotelRoomTypes.forEach(roomType => {
      // Generate random occupancy between 40% and 90%
      const occupancy = 0.4 + Math.random() * 0.5;
      const occupiedRooms = Math.round(roomType.inventory_count * occupancy);
      
      // Calculate revenue (base price with some randomness)
      const avgPrice = roomType.base_price * (0.9 + Math.random() * 0.3);
      const revenue = occupiedRooms * avgPrice;
      
      totalRevenue += revenue;
      totalRooms += roomType.inventory_count;
      totalOccupied += occupiedRooms;
      
      roomTypeBreakdown[roomType.id] = {
        room_type_id: roomType.id,
        room_type_name: roomType.name,
        revenue: Math.round(revenue * 100) / 100,
        rooms: roomType.inventory_count,
        occupied: occupiedRooms,
        occupancy_rate: Math.round(occupancy * 100) / 100
      };
    });
    
    const overallOccupancy = totalOccupied / totalRooms;
    
    analytics.push({
      date: groupDate.toISOString().split('T')[0],
      total_revenue: Math.round(totalRevenue * 100) / 100,
      total_rooms: totalRooms,
      total_occupied: totalOccupied,
      occupancy_rate: Math.round(overallOccupancy * 10000) / 10000,
      room_types: Object.values(roomTypeBreakdown)
    });
  }
  
  // Sort by date
  analytics.sort((a, b) => new Date(a.date) - new Date(b.date));
  
  return {
    hotel_id: hotelId,
    start_date: startDate.toISOString().split('T')[0],
    end_date: new Date(startDate.setDate(startDate.getDate() + days - 1)).toISOString().split('T')[0],
    group_by: groupBy,
    analytics: analytics
  };
};

// Mock API service
const mockApi = {
  // Authentication
  login: async (email, password) => {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Always return success for demo
    return {
      token: "mock-jwt-token",
      user: {
        id: 1,
        name: "Hotel Manager",
        email: email,
        role: "admin"
      }
    };
  },
  
  // Hotels
  getHotels: async () => {
    await new Promise(resolve => setTimeout(resolve, 500));
    return hotels;
  },
  
  getHotelById: async (id) => {
    await new Promise(resolve => setTimeout(resolve, 300));
    const hotel = hotels.find(h => h.id === parseInt(id));
    
    if (!hotel) {
      throw new Error("Hotel not found");
    }
    
    const hotelRoomTypes = roomTypes.filter(rt => rt.hotel_id === parseInt(id));
    
    return {
      ...hotel,
      room_types: hotelRoomTypes
    };
  },
  
  // Room Types
  getRoomTypes: async (hotelId = null) => {
    await new Promise(resolve => setTimeout(resolve, 400));
    
    if (hotelId) {
      return roomTypes.filter(rt => rt.hotel_id === parseInt(hotelId));
    }
    
    return roomTypes;
  },
  
  getRoomTypeById: async (id) => {
    await new Promise(resolve => setTimeout(resolve, 300));
    const roomType = roomTypes.find(rt => rt.id === parseInt(id));
    
    if (!roomType) {
      throw new Error("Room type not found");
    }
    
    return roomType;
  },
  
  // Pricing
  getPricingRecommendations: async (hotelId, startDate = new Date(), days = 30, roomTypeId = null) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const hotelRoomTypes = roomTypeId 
      ? roomTypes.filter(rt => rt.id === parseInt(roomTypeId) && rt.hotel_id === parseInt(hotelId))
      : roomTypes.filter(rt => rt.hotel_id === parseInt(hotelId));
    
    if (hotelRoomTypes.length === 0) {
      throw new Error("No room types found for the specified criteria");
    }
    
    const recommendations = {};
    
    hotelRoomTypes.forEach(roomType => {
      const pricingData = generatePricingData(roomType.id, startDate);
      
      recommendations[roomType.id] = {
        room_type_id: roomType.id,
        room_type_name: roomType.name,
        base_price: roomType.base_price,
        variable_cost: roomType.variable_cost,
        inventory_count: roomType.inventory_count,
        prices: pricingData
      };
    });
    
    return {
      hotel_id: parseInt(hotelId),
      start_date: startDate.toISOString().split('T')[0],
      days: days,
      generated_at: new Date().toISOString(),
      recommendations: recommendations
    };
  },
  
  // Analytics
  getRevenueAnalytics: async (hotelId, startDate = new Date(), endDate = null, roomTypeId = null, groupBy = "day") => {
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const days = endDate 
      ? Math.ceil((new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24))
      : 30;
    
    return generateRevenueAnalytics(parseInt(hotelId), new Date(startDate), days, groupBy);
  },
  
  getOccupancyAnalytics: async (hotelId, startDate = new Date(), endDate = null, roomTypeId = null, groupBy = "day") => {
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Reuse revenue analytics but focus on occupancy data
    const revenueData = await mockApi.getRevenueAnalytics(hotelId, startDate, endDate, roomTypeId, groupBy);
    
    return {
      ...revenueData,
      analytics: revenueData.analytics.map(item => ({
        date: item.date,
        total_rooms: item.total_rooms,
        total_occupied: item.total_occupied,
        occupancy_rate: item.occupancy_rate,
        room_types: item.room_types.map(rt => ({
          room_type_id: rt.room_type_id,
          room_type_name: rt.room_type_name,
          rooms: rt.rooms,
          occupied: rt.occupied,
          occupancy_rate: rt.occupancy_rate
        }))
      }))
    };
  },
  
  getContributionMarginAnalytics: async (hotelId, startDate = new Date(), endDate = null, roomTypeId = null, groupBy = "day") => {
    await new Promise(resolve => setTimeout(resolve, 900));
    
    const days = endDate 
      ? Math.ceil((new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24))
      : 30;
    
    const revenueData = await mockApi.getRevenueAnalytics(hotelId, startDate, endDate, roomTypeId, groupBy);
    const hotelRoomTypes = roomTypes.filter(rt => rt.hotel_id === parseInt(hotelId));
    
    return {
      ...revenueData,
      analytics: revenueData.analytics.map(item => {
        let totalVariableCost = 0;
        let totalContribution = 0;
        
        const roomTypesWithContribution = item.room_types.map(rt => {
          const roomType = hotelRoomTypes.find(r => r.id === rt.room_type_id);
          const variableCost = rt.occupied * roomType.variable_cost;
          const contribution = rt.revenue - variableCost;
          
          totalVariableCost += variableCost;
          totalContribution += contribution;
          
          return {
            ...rt,
            variable_cost: Math.round(variableCost * 100) / 100,
            contribution: Math.round(contribution * 100) / 100,
            contribution_margin: Math.round((contribution / rt.revenue) * 10000) / 10000
          };
        });
        
        const overallContributionMargin = totalContribution / item.total_revenue;
        
        return {
          date: item.date,
          total_revenue: item.total_revenue,
          total_variable_cost: Math.round(totalVariableCost * 100) / 100,
          total_contribution: Math.round(totalContribution * 100) / 100,
          contribution_margin: Math.round(overallContributionMargin * 10000) / 10000,
          total_rooms: item.total_rooms,
          total_occupied: item.total_occupied,
          room_types: roomTypesWithContribution
        };
      })
    };
  },
  
  // Dashboard data
  getDashboardData: async () => {
    await new Promise(resolve => setTimeout(resolve, 700));
    
    return {
      hotels: {
        count: hotels.length,
        active: hotels.filter(h => h.is_active).length,
      },
      rooms: {
        count: roomTypes.reduce((sum, rt) => sum + rt.inventory_count, 0),
        types: roomTypes.length,
      },
      revenue: {
        today: 2850,
        yesterday: 2450,
        change: 16.33,
      },
      occupancy: {
        today: 68,
        yesterday: 62,
        change: 9.68,
      },
      contribution: {
        today: 1950,
        yesterday: 1650,
        change: 18.18,
      },
      recentPriceChanges: [
        {
          id: 1,
          roomType: "Deluxe Suite",
          hotel: "Grand Hotel",
          oldPrice: 299,
          newPrice: 279,
          date: "2025-05-20",
        },
        {
          id: 2,
          roomType: "Standard Room",
          hotel: "City Center Hotel",
          oldPrice: 129,
          newPrice: 149,
          date: "2025-05-20",
        },
        {
          id: 3,
          roomType: "Executive Room",
          hotel: "Business Hotel",
          oldPrice: 189,
          newPrice: 169,
          date: "2025-05-19",
        },
      ],
      upcomingLowDemand: [
        {
          id: 1,
          date: "2025-06-10",
          hotel: "Grand Hotel",
          occupancy: 35,
          suggestedAction: "Price reduction recommended",
        },
        {
          id: 2,
          date: "2025-06-15",
          hotel: "City Center Hotel",
          occupancy: 42,
          suggestedAction: "Consider special offers",
        },
      ],
    };
  }
};

export default mockApi;
