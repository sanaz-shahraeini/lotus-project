# Celery Setup Guide for Windows

This guide provides instructions for setting up and running Celery with Redis on Windows for the Lotus project.

## Prerequisites

1. **Install Redis**
   
   You have two options for installing Redis:
   
   **Option A: Use the provided Redis MSI installer**
   - The Redis installer is included in your project: `Redis-x64-3.0.504.msi`
   - Double-click to install Redis
   - During installation, select the option to add Redis to your PATH
   - After installation, Redis server should start automatically as a Windows service
   
   **Option B: Download the latest version**
   - Download Redis for Windows from: https://github.com/tporadowski/redis/releases
   - Install and run the Redis server
   
   **Verify Redis is running**
   - Open Command Prompt and run: `redis-cli ping`
   - If Redis is running correctly, it should respond with: `PONG`

2. **Python Dependencies**
   Make sure you have these packages installed in your virtual environment:
   ```
   pip install celery django-celery-beat redis python-dotenv
   ```

## Environment Variables

The project uses a `.env` file for configuration. If you encounter issues with loading environment variables, the system will use default values.

If you want to customize the configuration, create a `.env` file in the project root with the following content:

```
# Database configuration
DATABASE_URL=postgres://postgres:your_password@localhost:5432/lotus

# Email configuration (if needed)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Debug settings
DEBUG=True
```

**Important:** Make sure the `.env` file is saved with UTF-8 encoding without BOM (Byte Order Mark).

## Running Celery

### Option 1: Using Batch Scripts (Recommended)

We've created three batch scripts to simplify running Celery:

1. **start_celery_worker.bat** - Starts the Celery worker process
2. **start_celery_beat.bat** - Starts the Celery beat scheduler
3. **start_all.bat** - Checks if Redis is running, then starts both worker and beat

To run Celery with all components:
1. Make sure Redis is running
2. Double-click `start_all.bat`

### Option 2: Running Manually

If you prefer to run Celery manually or need more control:

1. Open Command Prompt (not PowerShell)
2. Navigate to the project directory:
   ```
   cd D:\lotus1
   ```

3. Activate the virtual environment:
   ```
   venv\Scripts\activate.bat
   ```

4. Start the Celery worker:
   ```
   celery -A lotus worker --loglevel=info
   ```

5. In another Command Prompt window, repeat steps 2-3, then start Celery beat:
   ```
   celery -A lotus beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

## Troubleshooting

### Redis Connection Issues
- Ensure Redis server is running
- Check Redis connection with: `redis-cli ping`
- Verify Redis is listening on the default port (6379)

### Celery Won't Start
- Check logs in the `celery/` directory
- Ensure the virtual environment has all required packages
- Verify `CELERY_BROKER_URL` in settings.py is correct

### Module Not Found Errors
- If you see "ModuleNotFoundError: No module named 'checkLicense'", ensure the checkLicense.py file exists in the project root

## Monitoring Celery
- Check log files in the `celery/` directory
- Worker logs: celery_worker.log and celery_worker_err.log
- Beat logs: celery_beat.log and celery_beat_err.log

## Setting Up Periodic Tasks
- Periodic tasks are defined in the Alvand/tasks.py file
- You can also add/edit tasks through the Django admin interface under "Periodic Tasks"
- Access the admin at: http://localhost:8000/admin/django_celery_beat/periodictask/ 