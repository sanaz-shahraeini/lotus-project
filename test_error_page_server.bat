@echo off
echo Starting Django development server to test error page...
echo.
echo The error page will be available at: http://127.0.0.1:8000/errors/
echo.
echo Note: You'll need to login first at: http://127.0.0.1:8000/login/
echo Default credentials should be: supporter / DLqyS!5#dF13
echo.
pause
python manage.py runserver