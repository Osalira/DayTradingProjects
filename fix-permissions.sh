#!/bin/bash
echo "===================================="
echo "Day Trading System - Permission Fixer"
echo "===================================="
echo

# Store the root directory path
ROOT_DIR=$(pwd)

echo "Finding and fixing permissions for all shell scripts..."

# Use find to locate all shell scripts
echo "Fixing permissions in the backend directory..."
find ./backend -type f -name "*.sh" -exec chmod +x {} \; -exec echo "  Fixed: {}" \;

echo
echo "Fixing permissions for root shell scripts..."
chmod +x *.sh
for script in *.sh; do
    echo "  Fixed: $script"
done

# Fix permissions for Docker entrypoint scripts 
echo
echo "Checking Docker entrypoint scripts..."
for service_dir in backend/*-service; do
    if [ -d "$service_dir" ]; then
        if [ -f "$service_dir/docker-entrypoint.sh" ]; then
            chmod +x "$service_dir/docker-entrypoint.sh"
            echo "  Fixed: $service_dir/docker-entrypoint.sh"
        fi
    fi
done

echo
echo "Permissions fixed successfully!"
echo "Now you can run: docker compose down && docker compose up -d"
echo "====================================" 