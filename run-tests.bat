@echo off
ECHO ====================================
ECHO Day Trading System - Test Runner
ECHO ====================================
ECHO.

REM Check if JMeter is installed
where jmeter >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO JMeter is not installed or not in PATH. Please install JMeter before running tests.
    EXIT /B 1
)

REM Check if Docker is running
docker info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Docker is not running. Please start Docker before running tests.
    EXIT /B 1
)

REM Check if services are running, if not, start them
ECHO Checking if services are running...
docker ps --filter "name=backend_api-gateway" | findstr "api-gateway" >nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO Starting Docker services...
    cd backend && docker-compose up -d
    ECHO Services starting, waiting 15 seconds for them to initialize...
    timeout /t 15 /nobreak >nul
) ELSE (
    ECHO Services are already running.
)

ECHO.
ECHO Running JMeter tests...
ECHO.

REM Run the JMeter test and save results
jmeter -n -t Sample_test_script2.jmx -l test_result.jtl -j jmeter.log

ECHO.
ECHO Test completed.
ECHO Results saved to test_result.jtl
ECHO Logs saved to jmeter.log
ECHO.

REM Parse the results to show a summary
ECHO Test Summary:
type test_result.jtl | findstr /C:"true" > temp_success.txt
type test_result.jtl | findstr /C:"false" > temp_failures.txt
ECHO Successful requests: 
find /c /v "" < temp_success.txt
ECHO Failed requests: 
find /c /v "" < temp_failures.txt

REM Clean up temp files
del temp_success.txt
del temp_failures.txt

ECHO.
ECHO ====================================
ECHO Test Run Complete
ECHO ==================================== 