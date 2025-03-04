#!/bin/bash
echo "===================================="
echo "Day Trading System - Development Starter"
echo "===================================="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not found. Please install Docker before continuing."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Docker is not running. Please start Docker before continuing."
    exit 1
fi

echo "Starting backend services..."
cd backend && docker-compose up -d

echo
echo "Waiting for services to initialize..."
sleep 10

echo
echo "Starting frontend development server..."
cd ../frontend-monolith
npm run dev

echo
echo "Development environment is now running."
echo "- Backend services are running in Docker containers"
echo "- Frontend is running at http://localhost:5173/"
echo
echo "To stop, press Ctrl+C and then run ./stop-dev.sh"
echo "====================================" 