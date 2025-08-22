#!/usr/bin/env python
"""
Script to fix NULL created_at and updated_at dates in Errors table
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
sys.path.append('.')

try:
    django.setup()
    from Alvand.models import Errors
    from django.utils import timezone
    
    print("=== FIXING ERRORS TABLE DATES ===")
    
    # Check current state
    total_errors = Errors.objects.count()
    null_created = Errors.objects.filter(created_at__isnull=True).count()
    null_updated = Errors.objects.filter(updated_at__isnull=True).count()
    
    print(f"Total Errors records: {total_errors}")
    print(f"Records with NULL created_at: {null_created}")
    print(f"Records with NULL updated_at: {null_updated}")
    
    if null_created > 0 or null_updated > 0:
        print("\nUpdating NULL date fields...")
        
        # Update records with NULL created_at
        if null_created > 0:
            current_time = timezone.now()
            updated = Errors.objects.filter(created_at__isnull=True).update(created_at=current_time)
            print(f"✅ Updated {updated} records with NULL created_at")
        
        # Update records with NULL updated_at
        if null_updated > 0:
            current_time = timezone.now()
            updated = Errors.objects.filter(updated_at__isnull=True).update(updated_at=current_time)
            print(f"✅ Updated {updated} records with NULL updated_at")
    
    # Verify the fix
    remaining_null_created = Errors.objects.filter(created_at__isnull=True).count()
    remaining_null_updated = Errors.objects.filter(updated_at__isnull=True).count()
    
    if remaining_null_created == 0 and remaining_null_updated == 0:
        print("✅ All Errors records now have valid dates.")
    else:
        print(f"⚠️  Warning: {remaining_null_created} records still have NULL created_at")
        print(f"⚠️  Warning: {remaining_null_updated} records still have NULL updated_at")
    
    # Show updated data
    print("\nUpdated Errors records:")
    for error in Errors.objects.all():
        print(f"Code: {error.errorcodenum}, Created: {error.created_at}, Updated: {error.updated_at}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()