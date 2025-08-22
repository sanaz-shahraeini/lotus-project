@echo off
echo ========================================
echo    Alvand Data Import Tool
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Importing all Alvand CSV files...
echo.

echo 1. Importing Errors...
python import_alvand_errors.py
echo.

echo 2. Importing Infos...
python import_alvand_infos.py
echo.

echo 3. Importing Records...
python import_alvand_records.py
echo.

echo ========================================
echo    All imports completed!
echo ========================================
pause

