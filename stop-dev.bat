@echo off
ECHO ====================================
ECHO Day Trading System - Development Stopper
ECHO ====================================
ECHO.

ECHO Stopping backend services...
cd backend && docker-compose down

ECHO.
ECHO All services have been stopped.
ECHO ==================================== 