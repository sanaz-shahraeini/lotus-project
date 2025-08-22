@echo off
echo Starting Django development server...
cd %~dp0

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run Django server
python manage.py runserver 0.0.0.0:8000

pause