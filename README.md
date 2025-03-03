# Day Trading System

A microservices-based day trading platform that allows users to buy and sell stocks, manage their portfolio, and track their investment performance.

## System Architecture

The system consists of the following components:

### Frontend
- **frontend-monolith**: A React/TypeScript application providing a user interface for trading stocks.

### Backend
- **api-gateway**: Central entry point for all API requests, handles routing and authentication.
- **auth-service**: Manages user registration, login, and authentication.
- **trading-service**: Handles stock portfolio, wallet operations, and transaction history.
- **matching-engine**: Processes buy/sell orders and matches them with counterparties.
- **logging-service**: System-wide logging and auditing functionality.

## Prerequisites

- [Node.js](https://nodejs.org/) (v16 or higher)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [JMeter](https://jmeter.apache.org/download_jmeter.cgi) (for running tests)
- PostgreSQL (handled by Docker)

## Getting Started

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/DayTradingProjects.git
   cd DayTradingProjects
   ```

2. **Install dependencies**:
   ```bash
   # Frontend dependencies
   cd frontend-monolith
   npm install
   cd ..
   ```

### Development

1. **Start the development environment** (all services):
   ```
   start-dev.bat
   ```

   This will:
   - Start all backend services using Docker Compose
   - Start the frontend development server

2. **Stop the development environment**:
   ```
   stop-dev.bat
   ```

### Testing

Run the JMeter tests using:
```
run-tests.bat
```

This will:
- Verify if JMeter is installed
- Check if Docker is running
- Start the services if not already running
- Run the JMeter test script
- Display a summary of the test results

## Development Workflow

This project follows a Test-Driven Development (TDD) approach:

1. **Read the test**: Understand what the test in `Sample_test_script2.jmx` is checking.
2. **Run the test**: Execute `run-tests.bat` to see what's failing.
3. **Fix the issues**: Implement or modify code to make the test pass.
4. **Rerun the test**: Verify that your changes fixed the issue.
5. **Repeat**: Continue until all tests pass.

## Project Structure

```
/DayTradingProjects
├── frontend-monolith/         # React/TypeScript frontend
├── backend/
│    ├── auth-service/         # Authentication service
│    ├── trading-service/      # Trading operations service
│    ├── matching-engine/      # Order matching service (Go)
│    ├── logging-service/      # Logging service
│    ├── api-gateway/          # API Gateway
│    └── docker-compose.yml    # Docker configuration
├── Sample_test_script2.jmx    # JMeter test script
├── run-tests.bat              # Test runner script
├── start-dev.bat              # Development starter
└── stop-dev.bat               # Development stopper
```

## API Endpoints

### Authentication Service
- `POST /authentication/register` - Register a new user
- `POST /authentication/login` - Login and get JWT token

### Transaction Service
- `GET /transaction/getStockPrices` - Get current stock prices
- `GET /transaction/getStockPortfolio` - Get user's stock portfolio
- `GET /transaction/getStockTransactions` - Get stock transaction history
- `POST /transaction/addMoneyToWallet` - Add money to user's wallet
- `GET /transaction/getWalletBalance` - Get user's wallet balance
- `GET /transaction/getWalletTransactions` - Get wallet transaction history

### Matching Engine
- `POST /engine/placeStockOrder` - Place a buy/sell order
- `POST /engine/cancelStockTransaction` - Cancel a pending stock transaction

### Setup Endpoints
- `POST /setup/createStock` - Create a new stock
- `POST /setup/addStockToUser` - Add stock directly to a user's portfolio

## Docker Services

All backend services run in Docker containers. To manage them:

- **Start services**: `cd backend && docker-compose up -d`
- **Stop services**: `cd backend && docker-compose down`
- **View logs**: `cd backend && docker-compose logs -f [service-name]`
- **Rebuild service**: `cd backend && docker-compose build [service-name]`

## Troubleshooting

- **Services not starting**: Check Docker logs for errors
- **Database issues**: You may need to initialize the database with `docker-compose down -v` and restart to reset volumes
- **Port conflicts**: Ensure ports 4000-4004 and 5432 are available

## License

This project is licensed under the MIT License - see the LICENSE file for details.
