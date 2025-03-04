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
   git clone --recurse-submodules https://github.com/Osalira/DayTradingProjects.git
   cd DayTradingProjects
   ```

2. **Install dependencies**:
   ```bash
   # Frontend dependencies
   cd frontend-monolith
   npm install
   cd ..
   ```

3. **Make the shell scripts executable** (Linux/macOS only):
   ```bash
   chmod +x *.sh
   ```

4. **Fix Docker entrypoint permissions** (Linux/macOS only):
   ```bash
   # This step is crucial for Linux/macOS users to avoid "permission denied" errors
   cd backend
   find . -name "*.sh" -exec chmod +x {} \;
   cd ..
   ```

   > **IMPORTANT**: If you encounter a "permission denied" error when starting Docker containers, use the `fix-permissions.sh` script to quickly resolve the issue:
   > ```bash
   > # Only needed if you encounter "permission denied" errors
   > ./fix-permissions.sh
   > docker compose down
   > docker compose up -d
   > ```

### Development

#### Windows

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

#### Linux/macOS

1. **Start the development environment** (all services):
   ```
   ./start-dev.sh
   ```

   This will:
   - Start all backend services using Docker Compose
   - Start the frontend development server

2. **Stop the development environment**:
   ```
   ./stop-dev.sh
   ```

### Testing

#### Windows

Run the JMeter tests using:
```
run-tests.bat
```

#### Linux/macOS

Run the JMeter tests using:
```
./run-tests.sh
```

Both scripts will:
- Verify if JMeter is installed
- Check if Docker is running
- Start the services if not already running
- Run the JMeter test script
- Display a summary of the test results

### Automated Git Commits

#### Windows

Commit changes across all repositories:
```
commit-all.bat
```

#### Linux/macOS

Commit changes across all repositories:
```
./commit-all.sh
```

These scripts will:
- Increment a counter to track commit numbers
- Create a descriptive commit message
- Commit and push changes in all service directories

## Development Workflow

This project follows a Test-Driven Development (TDD) approach:

1. **Read the test**: Understand what the test in `Sample_test_script2.jmx` is checking.
2. **Run the test**: Execute the appropriate test script for your OS to see what's failing.
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
│
│   # Windows scripts
├── run-tests.bat              # Test runner script (Windows)
├── start-dev.bat              # Development starter (Windows)
├── stop-dev.bat               # Development stopper (Windows)
├── commit-all.bat             # Commit changes (Windows)
│
│   # Linux/macOS scripts
├── run-tests.sh               # Test runner script (Linux/macOS)
├── start-dev.sh               # Development starter (Linux/macOS)
├── stop-dev.sh                # Development stopper (Linux/macOS)
└── commit-all.sh              # Commit changes (Linux/macOS)
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

- **Start services**:
  - Windows: `cd backend && docker-compose up -d`
  - Linux/macOS: `cd backend && docker-compose up -d`
- **Stop services**:
  - Windows: `cd backend && docker-compose down`
  - Linux/macOS: `cd backend && docker-compose down`
- **View logs**:
  - Windows: `cd backend && docker-compose logs -f [service-name]`
  - Linux/macOS: `cd backend && docker-compose logs -f [service-name]`
- **Rebuild service**:
  - Windows: `cd backend && docker-compose build [service-name]`
  - Linux/macOS: `cd backend && docker-compose build [service-name]`

## Troubleshooting

- **Services not starting**: Check Docker logs for errors
- **Database issues**: You may need to initialize the database with `docker-compose down -v` and restart to reset volumes
- **Port conflicts**: Ensure ports 4000-4004 and 5432 are available

## Handling Permissions Issues

When working with this project across different operating systems (Windows, macOS, Linux), you may encounter permission issues with shell scripts, particularly when using Docker containers. This section explains how to identify and fix these issues.

### Common Permission Issues

1. **"Permission denied" errors when Docker tries to execute scripts**:
   ```
   Error: failed to create task for container: failed to create shim task: OCI runtime create failed: 
   runc create failed: unable to start container process: exec: "/app/docker-entrypoint.sh": permission denied
   ```

2. **Line ending issues**: Scripts with Windows-style line endings (CRLF) may fail in Linux containers.

### Using the Fix-Permissions Script

This project includes a comprehensive script for fixing permissions:

```bash
# Run this from the project root directory:
./fix-permissions.sh

# Then restart the containers:
cd backend
docker compose down
docker compose up -d
```

The script automatically:
- Sets executable permissions on all shell scripts
- Converts Windows (CRLF) line endings to Unix (LF) format 
- Fixes common Docker entrypoint scripts
- Checks Dockerfiles for proper permission handling

### Inside Container Fixes

If you need to fix permissions inside a running container:

```bash
# Copy the fix script into the container
docker cp docker-fix-permissions.sh container_name:/app/

# Execute the script in the container
docker exec -it container_name bash -c "chmod +x /app/docker-fix-permissions.sh && /app/docker-fix-permissions.sh"
```

### Preventing Future Issues

To prevent these issues in future development:

1. **Configure Git to handle line endings**:
   ```bash
   # For Unix/macOS users:
   git config --global core.autocrlf input
   
   # For Windows users:
   git config --global core.autocrlf true
   ```

2. **Use the `.gitattributes` file**: This project includes a `.gitattributes` file that enforces proper line endings for script files.

3. **Docker Best Practices**:
   - Always include `chmod +x` and `dos2unix` commands in Dockerfiles
   - Use the Alpine `dos2unix` package or `sed` commands to fix line endings
   - Test your Docker containers on different operating systems when possible

## License

This project is licensed under the MIT License - see the LICENSE file for details.
