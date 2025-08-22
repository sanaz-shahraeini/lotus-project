@echo off
echo Starting Alvand Errors Import...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the import script
python import_alvand_errors.py

REM Pause to see results
pause

