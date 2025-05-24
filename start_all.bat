@echo off
echo Starting all services...
cd %~dp0

echo Checking if Redis is running...
redis-cli ping > nul 2>&1
if errorlevel 1 (
    echo Redis is not running or not installed!
    echo.
    echo Installing Redis:
    echo 1. Run the Redis MSI installer included in this project: Redis-x64-3.0.504.msi
    echo 2. After installation, Redis should start automatically as a Windows service.
    echo 3. Verify with "redis-cli ping" in a new Command Prompt window
    echo.
    if exist Redis-x64-3.0.504.msi (
        echo Found Redis installer in the current directory.
        set /p install=Would you like to install Redis now? (y/n): 
        if /i "%install%"=="y" (
            echo Starting Redis installation...
            start "" "Redis-x64-3.0.504.msi"
            echo Please complete the installation and then run this script again.
            echo.
            pause
            exit /b
        )
    ) else (
        echo Redis installer not found in the current directory.
        echo You can download Redis for Windows from: https://github.com/tporadowski/redis/releases
    )
    echo.
    pause
    exit /b 1
) else (
    echo Redis is running! Continuing...
)

echo.
echo Starting Celery worker...
start cmd /k "call start_celery_worker.bat"

echo Starting Celery beat...
start cmd /k "call start_celery_beat.bat"

echo.
echo All services started!
echo You can check logs in the celery/ directory
echo.
echo Press any key to exit...
pause 