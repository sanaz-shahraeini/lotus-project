@echo off
echo Importing SMDR records from SMDR Report.txt into the database...
python manage.py import_smdr "d:\SMDR Report.txt" --force
pause 