#!/usr/bin/env python
"""
Script to clear all data from LotusDB
Usage: python clear_database.py
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.db import connection
from Alvand.models import (
    Connections, Costs, Countries, Device, Emailsending, Errors,
    Extensionsgroups, Faults, Groups, Infos, Permissions, Records,
    Telephons, Users, Verifications, PasswordResetRequest, Log,
    ContactInfo, errorsSent, lices, SMDRRecord
)

def clear_all_data():
    """Clear all data from all tables in LotusDB"""
    
    print("=" * 60)
    print("WARNING: This will delete ALL data from ALL tables in LotusDB!")
    print("This action cannot be undone.")
    print("=" * 60)
    
    confirm = input("Are you sure you want to proceed? (yes/no): ").lower().strip()
    
    if confirm != 'yes':
        print("Operation cancelled.")
        return
    
    # Get all models
    models_to_clear = [
        Connections, Costs, Countries, Device, Emailsending, Errors,
        Extensionsgroups, Faults, Groups, Infos, Permissions, Records,
        Telephons, Users, Verifications, PasswordResetRequest, Log,
        ContactInfo, errorsSent, lices, SMDRRecord
    ]
    
    # Disable foreign key checks temporarily (PostgreSQL specific)
    with connection.cursor() as cursor:
        cursor.execute("SET session_replication_role = replica;")
    
    try:
        total_deleted = 0
        
        for model in models_to_clear:
            try:
                count = model.objects.count()
                if count > 0:
                    model.objects.all().delete()
                    total_deleted += count
                    print(f"✓ Deleted {count} rows from {model._meta.db_table}")
                else:
                    print(f"  No data in {model._meta.db_table}")
            except Exception as e:
                print(f"✗ Error clearing {model._meta.db_table}: {str(e)}")
        
        print(f"\n🎉 Successfully deleted {total_deleted} total rows from all tables!")
        
    finally:
        # Re-enable foreign key checks
        with connection.cursor() as cursor:
            cursor.execute("SET session_replication_role = DEFAULT;")
    
    print("\n✅ Database clearing completed successfully!")

if __name__ == "__main__":
    clear_all_data()
