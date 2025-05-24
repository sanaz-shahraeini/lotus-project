@echo off
echo Importing records from records.py into the database with automatic 'y' response...
echo y | python manage.py import_records
pause 