@echo off
echo ============================================================
echo LotusDB Data Clearing Tool
echo ============================================================
echo.
echo This will delete ALL data from ALL tables in LotusDB!
echo This action cannot be undone.
echo.
echo Make sure you have:
echo 1. PostgreSQL running
echo 2. LotusDB database exists
echo 3. Virtual environment activated (if using one)
echo.
pause

echo.
echo Starting database clearing...
python clear_database.py

echo.
echo Press any key to exit...
pause > nul
