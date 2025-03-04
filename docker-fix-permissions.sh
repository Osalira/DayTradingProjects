#!/bin/bash
#
# Docker Fix Permissions Script
# Run this inside a container to fix permissions issues
#

echo "Checking and fixing script permissions inside container..."

# Fix all shell scripts in current directory
find . -name "*.sh" -type f -exec chmod +x {} \; -exec echo "Fixed permissions: {}" \;

# If dos2unix is available, fix line endings
if command -v dos2unix &> /dev/null; then
    echo "Converting Windows line endings (CRLF) to Unix format (LF)..."
    find . -name "*.sh" -type f -exec dos2unix {} \; -exec echo "Fixed line endings: {}" \;
else
    echo "dos2unix not found, skipping line ending conversion."
    echo "Consider installing dos2unix with: apt-get update && apt-get install -y dos2unix"
fi

# Verify shebang line in scripts
for script in $(find . -name "*.sh" -type f); do
    SHEBANG=$(head -n 1 "$script")
    echo "Script: $script - Shebang: $SHEBANG"
done

echo "Permissions fixed successfully!" 