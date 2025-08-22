#!/usr/bin/env python
"""
Script to fix NULL created_at dates in Faults table
Run this script to update existing records with NULL created_at values
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
sys.path.append('.')

try:
    django.setup()
    from Alvand.models import Faults
    from django.utils import timezone
    
    print("Checking Faults records with NULL created_at...")
    
    # Find records with NULL created_at
    null_created_records = Faults.objects.filter(created_at__isnull=True)
    count = null_created_records.count()
    
    if count == 0:
        print("✅ No records found with NULL created_at values.")
    else:
        print(f"Found {count} records with NULL created_at values.")
        
        # Update records - use date_time if available, otherwise use current time
        updated_count = 0
        for fault in null_created_records:
            if fault.date_time:
                # Use the existing date_time value
                fault.created_at = fault.date_time
            else:
                # Use current time as fallback
                fault.created_at = timezone.now()
            
            fault.save()
            updated_count += 1
        
        print(f"✅ Updated {updated_count} records successfully.")
    
    # Verify the fix
    remaining_null = Faults.objects.filter(created_at__isnull=True).count()
    if remaining_null == 0:
        print("✅ All Faults records now have valid created_at dates.")
    else:
        print(f"⚠️  Warning: {remaining_null} records still have NULL created_at values.")
    
    # Show some sample data
    print("\nSample of recent Faults records:")
    recent_faults = Faults.objects.order_by('-created_at')[:5]
    for fault in recent_faults:
        print(f"ID: {fault.id}, Error Code: {fault.errorcode}, "
              f"Date Time: {fault.date_time}, Created At: {fault.created_at}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure you're running this from the project root directory.")