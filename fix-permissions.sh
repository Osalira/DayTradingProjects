#!/bin/bash
echo "===================================="
echo "Day Trading System - Permission Fixer"
echo "===================================="
echo

# Store the root directory path
ROOT_DIR=$(pwd)

# Add a function to check if running on Windows
is_windows() {
    case "$(uname -s)" in
        CYGWIN*|MINGW*|MSYS*) return 0 ;;
        *) return 1 ;;
    esac
}

echo "Operating System Detection:"
if is_windows; then
    echo "  Windows detected - will use appropriate commands"
    # Windows may need different handling for certain operations
else
    echo "  Unix-like system detected"
fi
echo

echo "Finding and fixing permissions for all shell scripts..."

# Use find to locate all shell scripts
echo "Fixing permissions in the backend directory..."
find ./backend -type f -name "*.sh" -exec chmod +x {} \; -exec echo "  Fixed permissions: {}" \;

echo
echo "Converting Windows line endings (CRLF) to Unix format (LF)..."
find ./backend -type f -name "*.sh" -exec sed -i 's/\r$//' {} \; -exec echo "  Fixed line endings: {}" \;

echo
echo "Fixing permissions for root shell scripts..."
chmod +x *.sh
for script in *.sh; do
    echo "  Fixed permissions: $script"
    sed -i 's/\r$//' "$script"
    echo "  Fixed line endings: $script"
done

# Special focus on Docker entrypoint scripts
echo
echo "Special focus on Docker entrypoint scripts..."
for service_dir in backend/*-service; do
    if [ -d "$service_dir" ]; then
        if [ -f "$service_dir/docker-entrypoint.sh" ]; then
            chmod +x "$service_dir/docker-entrypoint.sh"
            sed -i 's/\r$//' "$service_dir/docker-entrypoint.sh"
            echo "  Fixed: $service_dir/docker-entrypoint.sh (permissions and line endings)"
            
            # Show first line to verify shebang
            SHEBANG=$(head -n 1 "$service_dir/docker-entrypoint.sh")
            echo "    Shebang: $SHEBANG"
        fi
    fi
done

# Fix init scripts
echo
echo "Fixing database initialization scripts..."
if [ -f "backend/init-multiple-dbs.sh" ]; then
    chmod +x backend/init-multiple-dbs.sh
    sed -i 's/\r$//' backend/init-multiple-dbs.sh
    echo "  Fixed: backend/init-multiple-dbs.sh (permissions and line endings)"
    
    # Show first line to verify shebang
    SHEBANG=$(head -n 1 backend/init-multiple-dbs.sh)
    echo "    Shebang: $SHEBANG"
fi

# Fix matching-engine specific scripts
if [ -d "backend/matching-engine" ]; then
    echo
    echo "Fixing matching-engine scripts..."
    chmod +x backend/matching-engine/*.sh
    find backend/matching-engine -name "*.sh" -exec sed -i 's/\r$//' {} \; -exec echo "  Fixed: {}" \;
fi

# Verify and fix Dockerfiles
echo
echo "Checking Dockerfiles for permission-setting commands..."
grep -l "docker-entrypoint.sh" $(find ./backend -name Dockerfile) | while read dockerfile; do
    if ! grep -q "chmod +x" "$dockerfile"; then
        echo "  Warning: $dockerfile might need 'chmod +x' added for scripts"
    else
        echo "  ✓ $dockerfile already has chmod +x commands"
    fi
    
    if ! grep -q "dos2unix" "$dockerfile"; then
        echo "  Warning: $dockerfile might need 'dos2unix' added for line endings"
    else
        echo "  ✓ $dockerfile already has dos2unix commands"
    fi
done

echo
echo "Permissions fixed successfully!"
echo "Use these commands to restart your containers:"
echo "  cd backend"
echo "  docker compose down"
echo "  docker compose up -d"
echo

# Recommendations to prevent future issues
echo "To prevent similar issues in the future, consider:"
echo "1. Setting core.autocrlf in Git:"
echo "   git config --global core.autocrlf input"
echo
echo "2. Adding .gitattributes file with:"
echo "   *.sh text eol=lf"
echo "   *.md text eol=lf"
echo "   Dockerfile text eol=lf"
echo
echo "3. Adding a pre-commit hook to check for executable permissions"
echo "====================================" 