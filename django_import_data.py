#!/usr/bin/env python
"""
Django-based data import script
This imports data exported by django_export_data.py
"""

import os
import sys
import django
import json
import glob
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.core import serializers
from django.db import transaction

def find_latest_export():
    """Find the most recent data export file"""
    export_files = glob.glob("lotus_data_export_*.json")
    if not export_files:
        return None
    return max(export_files, key=os.path.getctime)

def import_data(export_file):
    """Import data from JSON export file"""
    print(f"📁 Loading data from: {export_file}")
    
    with open(export_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Found {len(data)} objects to import")
    
    # Import data in a transaction
    try:
        with transaction.atomic():
            # Deserialize and save objects
            objects = serializers.deserialize('json', json.dumps(data))
            imported_count = 0
            
            for obj in objects:
                try:
                    obj.save()
                    imported_count += 1
                    if imported_count % 100 == 0:
                        print(f"⏳ Imported {imported_count} objects...")
                except Exception as e:
                    print(f"⚠️  Warning: Could not import {obj.object}: {e}")
            
            print(f"✅ Successfully imported {imported_count} objects")
            return True
            
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Django-based data import...")
    
    # Find the latest export file
    export_file = find_latest_export()
    if not export_file:
        print("❌ No export file found! Please run django_export_data.py first.")
        sys.exit(1)
    
    print(f"📁 Found export file: {export_file}")
    
    # Import data
    success = import_data(export_file)
    
    if success:
        print(f"\n🎉 Data import completed successfully!")
        print("Your local database now has all the data from Neon.")
    else:
        print("\n❌ Import failed. Check error messages above.")
