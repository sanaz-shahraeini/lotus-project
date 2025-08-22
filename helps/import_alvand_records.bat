@echo off
echo Starting Alvand Records Import...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the import script
python import_alvand_records.py

REM Pause to see results
pause
