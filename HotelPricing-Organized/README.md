# Hotel Dynamic Pricing Engine SaaS - Organized Version

A smart, high-end SaaS platform designed for independent hotels to dynamically price rooms during low-demand periods. It leverages real-time demand forecasting and contribution margin logic to determine optimal pricing — even allowing rooms to be sold at a loss, so long as contribution margins remain positive.

## Core Principle

**Contribution Margin Logic:**  
Room is considered viable for discounted sale if:

```
Room Price - Variable Cost per Room > 0
```

This ensures each sale contributes to covering fixed costs like staff salaries, utilities, and property expenses — improving overall profitability through occupancy.

## Architecture

### MVP Modules (Phase 1)
1. **Room-Level Dynamic Pricing Engine** - Real-time pricing suggestions by room type
2. **Demand Forecasting Module** - Uses ML regression to forecast demand
3. **Property & Cost Configuration Dashboard** - Input fixed costs, variable costs per room
4. **Admin Analytics Panel** - Real-time and historical views of revenue, occupancy, and margins

## Tech Stack

- **Frontend:** React.js + Tailwind CSS
- **Backend:** Python (FastAPI)
- **Forecasting:** Facebook Prophet / XGBoost
- **Database:** PostgreSQL
- **Infrastructure:** Docker, Docker Compose
- **Authentication:** Auth0 (configurable)

## Project Structure

```
hotel-dynamic-pricing/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── db/             # Database models and migrations
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── .env.example        # Environment variables template
│   ├── requirements.txt    # Python dependencies
│   └── run.py              # Script to run the application
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── contexts/       # React contexts
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service calls
│   │   ├── store/          # State management
│   │   ├── styles/         # Global styles
│   │   ├── utils/          # Utility functions
│   │   └── App.js          # Main application component
│   ├── nginx.conf          # Nginx configuration for production
│   └── package.json        # Node.js dependencies
├── Dockerfile.backend      # Dockerfile for backend
├── Dockerfile.frontend     # Dockerfile for frontend
├── docker-compose.yml      # Docker Compose configuration
├── deploy.sh               # Deployment script
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Node.js 16+ (for local frontend development)
- Python 3.9+ (for local backend development)
- PostgreSQL 13+ (for local database)

### Local Development Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your database credentials and other configuration.

5. Run the backend server:
   ```
   python run.py
   ```
   The API will be available at http://localhost:8000 and the API documentation at http://localhost:8000/docs.

#### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The frontend will be available at http://localhost:3000.

### Containerized Deployment

1. Make sure Docker and Docker Compose are installed on your system.

2. Create a `.env` file in the backend directory:
   ```
   cp backend/.env.example backend/.env
   ```
   Edit the `.env` file with your configuration.

3. Run the deployment script:
   ```
   chmod +x deploy.sh
   ./deploy.sh
   ```
   This will build and start all the necessary containers.

4. Access the application at http://localhost and the API documentation at http://localhost/api/v1/docs.

## Key Features

### Dynamic Pricing Engine
- Real-time pricing suggestions based on demand forecasts
- Cost-based pricing floors using contribution margin logic
- Override capability with manager notes
- Support for multiple currencies

### Demand Forecasting
- ML-based demand prediction using historical data
- Seasonality pattern recognition
- Price elasticity simulation
- External event calendar integration

### Property & Cost Configuration
- Fixed and variable cost management
- Room type and inventory management
- Business rule configuration
- Tax and service charge settings

### Analytics Dashboard
- Revenue analytics with trends and comparisons
- Occupancy tracking and forecasting
- Contribution margin analysis
- Pricing performance evaluation

## License

This project is proprietary and confidential.

## Contact

For support or inquiries, please contact support@hoteldynamicpricing.com

## Architecture

### MVP Modules (Phase 1)
1. **Room-Level Dynamic Pricing Engine**
2. **Demand Forecasting Module**
3. **Property & Cost Configuration Dashboard**
4. **Admin Analytics Panel**

## Tech Stack

- **Frontend:** React.js + Tailwind CSS
- **Backend:** Python (FastAPI)
- **Forecasting:** Facebook Prophet / XGBoost
- **Database:** PostgreSQL
- **Infrastructure:** AWS (EC2 + RDS), S3 for static storage
- **Authentication:** Auth0
- **APIs:** REST
- **CI/CD:** GitHub Actions + Docker

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.9+)
- PostgreSQL (v13+)
- Docker (optional)

### Installation

#### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your database credentials and other configuration.

5. Run migrations:
   ```
   alembic upgrade head
   ```

6. Start the backend server:
   ```
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

## Project Structure

```
hotel-dynamic-pricing/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── db/             # Database models and migrations
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── tests/              # Test suite
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service calls
│   │   ├── store/          # State management
│   │   ├── styles/         # Global styles
│   │   ├── utils/          # Utility functions
│   │   └── App.js          # Main application component
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind CSS configuration
└── docs/                   # Documentation
```

## License

This project is proprietary and confidential.

## Contact

For support or inquiries, please contact support@hoteldynamicpricing.com
