# Dashboard Records Import Instructions

## What's Available

- 2101 call records have been successfully imported from `records.py` to the database
- The system uses an improved dashboard with better filtering and performance

## How to Access the Dashboard

1. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. Visit the dashboard directly:
   ```
   http://localhost:8000/
   ```

   Or use the specific dashboard URL:
   ```
   http://localhost:8000/dashboard-improved/
   ```

## Dashboard Features

The dashboard provides:

- Pagination with 20 records per page
- Filtering by:
  - Call type (نوع تماس)
  - Extension (داخلی)
  - Urban line (خط شهری)
  - Date range (از تاریخ - تا تاریخ)
- Contact numbers are properly displayed

## Reimporting Records

If you need to reimport the records:

```
.\import_records.bat
```

This will delete all existing records and import fresh records from `records.py`.

## Accessing via Root URL

For convenience, the application's root URL (`/`) redirects directly to the improved dashboard page. 