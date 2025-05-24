# Call Records Dashboard

This module provides functionality to import call records from a Python file into the Django database and display them in a dashboard.

## Features

- Import call records from a records.py file into the database
- View call records in a paginated dashboard
- Filter records by call type, extension, urban line, and date range
- Improved performance with optimized database queries

## How to Import Records

1. Make sure your records.py file contains a variable named `records` with call record data
2. Run the import script:

```
import_records.bat
```

Or use the Django management command directly:

```
python manage.py import_records
```

## Accessing the Dashboard

Two dashboard versions are available:

1. Original Dashboard: `/dashboard/`
2. Improved Dashboard: `/dashboard-improved/`

The improved dashboard offers better performance and more reliable filtering.

## Dashboard Filtering Options

The dashboard allows you to filter records by:

- **Call Type**: Filter by incoming, outgoing, or internal calls
- **Extension**: Filter by specific internal extensions
- **Urban Line**: Filter by specific urban lines
- **Date Range**: Filter by start and end dates

## Data Structure

Each call record contains the following information:

- Date and time of the call
- Extension number
- Urban line used
- Contact number
- Call type (incoming, outgoing, internal, etc.)
- Call duration
- Other metadata

## Troubleshooting

If you encounter issues:

1. Make sure your records.py file is in the correct format
2. Check that the database has sufficient space
3. Verify that your Django migrations are up to date
4. Check the logs for any import errors

For any further questions, please contact the system administrator. 