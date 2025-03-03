@echo off
ECHO ====================================
ECHO Day Trading System - Development Starter
ECHO ====================================
ECHO.

REM Check if Docker is installed
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Docker is not running. Please start Docker before continuing.
    EXIT /B 1
)

ECHO Starting backend services...
cd backend && docker-compose up -d

ECHO.
ECHO Waiting for services to initialize...
timeout /t 10 /nobreak >nul

ECHO.
ECHO Starting frontend development server...
cd ../frontend-monolith
npm run dev

ECHO.
ECHO Development environment is now running.
ECHO - Backend services are running in Docker containers
ECHO - Frontend is running at http://localhost:5173/
ECHO.
ECHO To stop, press Ctrl+C and then run stop-dev.bat
ECHO ==================================== 