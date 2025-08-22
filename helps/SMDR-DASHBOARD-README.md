# SMDR Dashboard Instructions

## Overview

The SMDR (Station Message Detail Recording) Dashboard provides a visual interface for viewing and analyzing phone call records from your PBX system. This dashboard allows you to filter and search through call records to get insights into your organization's communication patterns.

## Features

- Display of all SMDR call records with pagination
- Comprehensive filtering options:
  - Call type (incoming, outgoing, internal, system messages)
  - Extension numbers
  - CO lines (urban lines)
  - Date range
  - Phone number search
- Statistics dashboard showing call counts by type
- Print-friendly design

## How to Import SMDR Data

1. Make sure your SMDR report file is located at `d:\SMDR Report.txt`
2. Run the import script:
   ```
   import_smdr.bat
   ```

   Or use the Django management command directly:
   ```
   python manage.py import_smdr "d:\SMDR Report.txt" --force
   ```

3. The script will parse the SMDR report file and import all records into the database

## Accessing the Dashboard

1. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. Visit the SMDR dashboard:
   ```
   http://localhost:8000/image.png
   ```

## Using the Dashboard

### Filtering Records

- **Call Type**: Select one or more call types (incoming, outgoing, internal, system)
- **Extension**: Filter by specific extension numbers
- **CO (Urban Line)**: Filter by specific CO lines
- **Search**: Enter a phone number to search for specific calls
- **Date Range**: Set a date range to filter calls within a specific period

### Viewing Statistics

The top of the dashboard displays statistics about your call records:
- Total number of calls
- Number of incoming calls
- Number of outgoing calls
- Number of internal calls
- Number of system messages

### Navigating Pages

If there are many records, they will be paginated. Use the navigation buttons at the bottom of the page to move between pages.

### Printing Reports

Click the "Print" button to print the current view of the dashboard, which includes all applied filters.

## Troubleshooting

If you encounter issues:

1. Ensure your SMDR report file is in the correct format
2. Check that the database migrations are up to date:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Check for any error messages during the import process
4. Verify that your SMDR file is accessible at the specified path

## Support

For any further assistance, please contact the system administrator. 