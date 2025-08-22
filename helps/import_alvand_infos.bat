@echo off
echo Starting Alvand Infos Import...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the import script
python import_alvand_infos.py

REM Pause to see results
pause

