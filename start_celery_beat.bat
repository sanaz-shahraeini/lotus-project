@echo off
echo Starting Celery beat...
cd %~dp0
set PYTHONPATH=%~dp0
set DJANGO_SETTINGS_MODULE=lotus.settings

:: Activate virtual environment if using one
call venv\Scripts\activate.bat

:: Start Celery beat
celery -A lotus beat --loglevel=info --logfile=celery/celery_beat.log --pidfile=celery/celery_beat.pid --scheduler django_celery_beat.schedulers:DatabaseScheduler

pause 