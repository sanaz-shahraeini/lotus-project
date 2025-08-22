#!/usr/bin/env python
"""
Script to check the current state of Faults table
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
sys.path.append('.')

try:
    django.setup()
    from Alvand.models import Faults, Errors
    
    print("=== FAULTS TABLE ANALYSIS ===")
    
    # Check total count
    total_faults = Faults.objects.count()
    print(f"Total Faults records: {total_faults}")
    
    if total_faults > 0:
        # Check for NULL values
        null_date_time = Faults.objects.filter(date_time__isnull=True).count()
        null_created_at = Faults.objects.filter(created_at__isnull=True).count()
        
        print(f"Records with NULL date_time: {null_date_time}")
        print(f"Records with NULL created_at: {null_created_at}")
        
        # Show all records
        print("\nAll Faults records:")
        for fault in Faults.objects.all()[:10]:  # Show first 10
            print(f"ID: {fault.id}, Error Code: {fault.errorcode}, "
                  f"Date Time: {fault.date_time}, Created At: {fault.created_at}, "
                  f"Label: {fault.label}")
    else:
        print("No Faults records found in database.")
        print("\nLet's create some test data to demonstrate the fix...")
        
        # Create test fault records
        from django.utils import timezone
        import datetime
        
        # Create a fault with date_time
        fault1 = Faults.objects.create(
            errorcode=537,
            date_time=timezone.now() - datetime.timedelta(days=1),
            label="Test Error 1"
        )
        
        # Create a fault without date_time (will use created_at)
        fault2 = Faults.objects.create(
            errorcode=538,
            label="Test Error 2"
        )
        
        print(f"Created test fault 1: ID {fault1.id}")
        print(f"Created test fault 2: ID {fault2.id}")
    
    print("\n=== ERRORS TABLE ANALYSIS ===")
    total_errors = Errors.objects.count()
    print(f"Total Errors records: {total_errors}")
    
    if total_errors > 0:
        print("\nSample Error records:")
        for error in Errors.objects.all()[:5]:
            print(f"Code: {error.errorcodenum}, Message: {error.errormessage[:50]}...")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()