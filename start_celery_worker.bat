@echo off
echo Starting Celery worker...
cd %~dp0
set PYTHONPATH=%~dp0
set DJANGO_SETTINGS_MODULE=lotus.settings

:: Activate virtual environment if using one
call venv\Scripts\activate.bat

:: Start Celery worker
celery -A lotus worker --loglevel=info --logfile=celery/celery_worker.log --pidfile=celery/celery_worker.pid

pause 