#!/bin/bash
echo "===================================="
echo "Day Trading System - Commit All Changes"
echo "===================================="
echo

# Store the root directory path
ROOT_DIR=$(pwd)

# Define the counter file path
COUNTER_FILE=.commit_counter

# Check if counter file exists, create if it doesn't
if [ ! -f "$COUNTER_FILE" ]; then
    echo 0 > "$COUNTER_FILE"
    echo "Initialized commit counter file"
fi

# Read current counter and increment it
COUNTER=$(cat "$COUNTER_FILE")
COUNTER=$((COUNTER + 1))

# Save the new counter value
echo $COUNTER > "$COUNTER_FILE"

# Determine ordinal suffix
SUFFIX="th"
if [ $COUNTER -eq 1 ]; then
    SUFFIX="st"
elif [ $COUNTER -eq 2 ]; then
    SUFFIX="nd"
elif [ $COUNTER -eq 3 ]; then
    SUFFIX="rd"
elif [ $COUNTER -gt 20 ]; then
    LAST_DIGIT=$((COUNTER % 10))
    if [ $LAST_DIGIT -eq 1 ]; then
        SUFFIX="st"
    elif [ $LAST_DIGIT -eq 2 ]; then
        SUFFIX="nd"
    elif [ $LAST_DIGIT -eq 3 ]; then
        SUFFIX="rd"
    fi
fi

# Construct commit message
COMMIT_MSG="${COUNTER}${SUFFIX} frontend fixes"

# Define array of directories to process
DIRS=(
    "frontend-monolith"
    "backend/auth-service"
    "backend/trading-service"
    "backend/matching-engine"
    "backend/logging-service"
    "backend/api-gateway"
)

echo
echo "Starting commit process with message: \"$COMMIT_MSG\""
echo

# Loop through directories and commit changes
for DIR in "${DIRS[@]}"; do
    echo "Processing $DIR..."
    
    # Check if directory exists
    if [ -d "$DIR" ]; then
        cd "$DIR"
        
        # Check if it's a git repository
        if [ -d ".git" ]; then
            echo "  Staging changes..."
            git add .
            
            echo "  Committing changes..."
            git commit -m "$COMMIT_MSG"
            
            echo "  Pushing changes to remote..."
            git push
            
            echo "  Done with $DIR"
        else
            echo "  Warning: $DIR is not a git repository"
        fi
        
        # Return to root directory
        cd "$ROOT_DIR"
    else
        echo "  Warning: Directory $DIR not found"
    fi
    echo
done

echo "All repositories processed"
echo "New commit counter: $COUNTER" 