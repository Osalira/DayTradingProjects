#!/bin/bash
echo "===================================="
echo "Day Trading System - Test Runner"
echo "===================================="
echo

# Check if JMeter is installed
if ! command -v jmeter &> /dev/null; then
    echo "JMeter is not installed or not in PATH. Please install JMeter before running tests."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Docker is not running. Please start Docker before running tests."
    exit 1
fi

# Check if services are running, if not, start them
echo "Checking if services are running..."
if ! docker ps --filter "name=backend_api-gateway" | grep "api-gateway" &> /dev/null; then
    echo "Starting Docker services..."
    cd backend && docker-compose up -d
    echo "Services starting, waiting 15 seconds for them to initialize..."
    sleep 15
else
    echo "Services are already running."
fi

echo
echo "Running JMeter tests..."
echo

# Run the JMeter test and save results
jmeter -n -t Sample_test_script2.jmx -l test_result.jtl -j jmeter.log

echo
echo "Test completed."
echo "Results saved to test_result.jtl"
echo "Logs saved to jmeter.log"
echo

# Parse the results to show a summary
echo "Test Summary:"
success_count=$(grep -c "true" test_result.jtl)
failure_count=$(grep -c "false" test_result.jtl)
echo "Successful requests: $success_count"
echo "Failed requests: $failure_count"

echo
echo "===================================="
echo "Test Run Complete"
echo "====================================" 