import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  BuildingOfficeIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  ArrowUpIcon,
  ArrowDownIcon,
} from '@heroicons/react/24/outline';

const DashboardHome = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    // In a real application, you would fetch data from your API
    // For demo purposes, we'll simulate API data
    const fetchDashboardData = async () => {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock data
        const mockData = {
          hotels: {
            count: 3,
            active: 3,
          },
          rooms: {
            count: 12,
            types: 4,
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
              roomType: 'Deluxe Suite',
              hotel: 'Grand Hotel',
              oldPrice: 299,
              newPrice: 279,
              date: '2025-05-20',
            },
            {
              id: 2,
              roomType: 'Standard Room',
              hotel: 'City Center Hotel',
              oldPrice: 129,
              newPrice: 149,
              date: '2025-05-20',
            },
            {
              id: 3,
              roomType: 'Executive Room',
              hotel: 'Business Hotel',
              oldPrice: 189,
              newPrice: 169,
              date: '2025-05-19',
            },
          ],
          upcomingLowDemand: [
            {
              id: 1,
              date: '2025-06-10',
              hotel: 'Grand Hotel',
              occupancy: 35,
              suggestedAction: 'Price reduction recommended',
            },
            {
              id: 2,
              date: '2025-06-15',
              hotel: 'City Center Hotel',
              occupancy: 42,
              suggestedAction: 'Consider special offers',
            },
          ],
        };
        
        setDashboardData(mockData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full py-24">
        <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
          Welcome to your Hotel Dynamic Pricing Dashboard
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 mb-8">
        {/* Hotels & Rooms */}
        <div className="card">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BuildingOfficeIcon className="h-10 w-10 text-primary-600 dark:text-primary-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    Hotels & Rooms
                  </dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900 dark:text-white">
                      {dashboardData.hotels.count} Hotels / {dashboardData.rooms.count} Rooms
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 px-5 py-3">
            <div className="text-sm">
              <Link
                to="/hotels"
                className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300"
              >
                View all hotels
              </Link>
            </div>
          </div>
        </div>

        {/* Revenue */}
        <div className="card">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CurrencyDollarIcon className="h-10 w-10 text-primary-600 dark:text-primary-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    Today's Revenue
                  </dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900 dark:text-white">
                      ${dashboardData.revenue.today.toLocaleString()}
                    </div>
                    <div className="flex items-center text-sm">
                      {dashboardData.revenue.change > 0 ? (
                        <>
                          <ArrowUpIcon className="h-4 w-4 text-success-500" />
                          <span className="text-success-600 dark:text-success-400">
                            {dashboardData.revenue.change}% from yesterday
                          </span>
                        </>
                      ) : (
                        <>
                          <ArrowDownIcon className="h-4 w-4 text-danger-500" />
                          <span className="text-danger-600 dark:text-danger-400">
                            {Math.abs(dashboardData.revenue.change)}% from yesterday
                          </span>
                        </>
                      )}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 px-5 py-3">
            <div className="text-sm">
              <Link
                to="/analytics/revenue"
                className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300"
              >
                View revenue analytics
              </Link>
            </div>
          </div>
        </div>

        {/* Occupancy */}
        <div className="card">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-10 w-10 text-primary-600 dark:text-primary-400" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                    Today's Occupancy
                  </dt>
                  <dd>
                    <div className="text-lg font-medium text-gray-900 dark:text-white">
                      {dashboardData.occupancy.today}%
                    </div>
                    <div className="flex items-center text-sm">
                      {dashboardData.occupancy.change > 0 ? (
                        <>
                          <ArrowUpIcon className="h-4 w-4 text-success-500" />
                          <span className="text-success-600 dark:text-success-400">
                            {dashboardData.occupancy.change}% from yesterday
                          </span>
                        </>
                      ) : (
                        <>
                          <ArrowDownIcon className="h-4 w-4 text-danger-500" />
                          <span className="text-danger-600 dark:text-danger-400">
                            {Math.abs(dashboardData.occupancy.change)}% from yesterday
                          </span>
                        </>
                      )}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 px-5 py-3">
            <div className="text-sm">
              <Link
                to="/analytics/occupancy"
                className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300"
              >
                View occupancy analytics
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Price Changes */}
      <div className="mb-8">
        <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Recent Price Changes</h2>
        <div className="card">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Room Type
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Hotel
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Old Price
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    New Price
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Change
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {dashboardData.recentPriceChanges.map((change) => (
                  <tr key={change.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      {change.roomType}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {change.hotel}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      ${change.oldPrice}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      ${change.newPrice}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {change.newPrice > change.oldPrice ? (
                        <span className="text-success-600 dark:text-success-400 flex items-center">
                          <ArrowUpIcon className="h-4 w-4 mr-1" />
                          {(((change.newPrice - change.oldPrice) / change.oldPrice) * 100).toFixed(1)}%
                        </span>
                      ) : (
                        <span className="text-danger-600 dark:text-danger-400 flex items-center">
                          <ArrowDownIcon className="h-4 w-4 mr-1" />
                          {(((change.oldPrice - change.newPrice) / change.oldPrice) * 100).toFixed(1)}%
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {change.date}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 px-5 py-3">
            <div className="text-sm">
              <Link
                to="/pricing"
                className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300"
              >
                View all price changes
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Upcoming Low Demand Periods */}
      <div className="mb-8">
        <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Upcoming Low Demand Periods</h2>
        <div className="card">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Hotel
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Forecasted Occupancy
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Suggested Action
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {dashboardData.upcomingLowDemand.map((period) => (
                  <tr key={period.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      {period.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {period.hotel}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      <span className="text-danger-600 dark:text-danger-400">{period.occupancy}%</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      {period.suggestedAction}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 px-5 py-3">
            <div className="text-sm">
              <Link
                to="/forecasting"
                className="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300"
              >
                View demand forecasts
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <Link
            to="/pricing"
            className="card p-6 hover:shadow-card-hover transition-shadow duration-300"
          >
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Update Pricing</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Review and update dynamic pricing for your properties
            </p>
          </Link>
          
          <Link
            to="/forecasting"
            className="card p-6 hover:shadow-card-hover transition-shadow duration-300"
          >
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">View Forecasts</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Check demand forecasts and optimize your pricing strategy
            </p>
          </Link>
          
          <Link
            to="/analytics/contribution-margin"
            className="card p-6 hover:shadow-card-hover transition-shadow duration-300"
          >
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Analyze Margins</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Review contribution margins and profitability metrics
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;
