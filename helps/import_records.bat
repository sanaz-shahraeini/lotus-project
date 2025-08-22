@echo off
echo Importing records from records.py into the database...
python manage.py import_records --force
pause 