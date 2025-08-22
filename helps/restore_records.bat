@echo off
echo ============================================================
echo Lotus Records Table Restoration Tool
echo ============================================================
echo.
echo This will restore the Alvand_records table and import data from CSV.
echo.
echo Make sure you have:
echo 1. PostgreSQL running
echo 2. LotusDB database exists
echo 3. Alvand_records.csv file in the current directory
echo 4. Virtual environment activated (if using one)
echo.
pause

echo.
echo Starting records table restoration...
python restore_records_table.py

echo.
echo Press any key to exit...
pause > nul
