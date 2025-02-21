@echo off
setlocal enabledelayedexpansion

:: Store the root directory path
set "ROOT_DIR=%CD%"

:: Define the counter file path
set "COUNTER_FILE=.commit_counter"

:: Check if counter file exists, create if it doesn't
if not exist "%COUNTER_FILE%" (
    echo 0 > "%COUNTER_FILE%"
    echo Initialized commit counter file
)

:: Read current counter and increment it
set /p COUNTER=<"%COUNTER_FILE%"
set /a "COUNTER+=1"

:: Save the new counter value
echo %COUNTER% > "%COUNTER_FILE%"

:: Determine ordinal suffix
set "SUFFIX=th"
if %COUNTER% EQU 1 set "SUFFIX=st"
if %COUNTER% EQU 2 set "SUFFIX=nd"
if %COUNTER% EQU 3 set "SUFFIX=rd"
if %COUNTER% GTR 20 (
    set "LAST_DIGIT=%COUNTER:~-1%"
    if !LAST_DIGIT! EQU 1 set "SUFFIX=st"
    if !LAST_DIGIT! EQU 2 set "SUFFIX=nd"
    if !LAST_DIGIT! EQU 3 set "SUFFIX=rd"
)

:: Construct commit message
set "COMMIT_MSG=%COUNTER%%SUFFIX% commit"

:: Define array of directories to process
set "DIRS[0]=frontend-monolith"
set "DIRS[1]=backend\auth-service"
set "DIRS[2]=backend\trading-service"
set "DIRS[3]=backend\matching-engine"
set "DIRS[4]=backend\logging-service"
set "DIRS[5]=backend\api-gateway"

echo.
echo Starting commit process with message: "%COMMIT_MSG%"
echo.

:: Loop through directories and commit changes
for /L %%i in (0,1,5) do (
    set "DIR=!DIRS[%%i]!"
    echo Processing !DIR!...
    
    :: Check if directory exists
    if exist "!DIR!" (
        cd "!DIR!"
        
        :: Check if it's a git repository
        if exist ".git" (
            echo   Staging changes...
            git add .
            
            echo   Committing changes...
            git commit -m "%COMMIT_MSG%"
            
            echo   Done with !DIR!
        ) else (
            echo   Warning: !DIR! is not a git repository
        )
        
        :: Return to root directory
        cd "%ROOT_DIR%"
    ) else (
        echo   Warning: Directory !DIR! not found
    )
    echo.
)

echo All repositories processed
echo New commit counter: %COUNTER%

endlocal 