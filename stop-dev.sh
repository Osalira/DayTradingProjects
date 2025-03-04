#!/bin/bash
echo "===================================="
echo "Day Trading System - Development Stopper"
echo "===================================="
echo

echo "Stopping backend services..."
cd backend && docker-compose down

echo
echo "All services have been stopped."
echo "====================================" 