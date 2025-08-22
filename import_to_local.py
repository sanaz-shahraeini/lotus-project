#!/usr/bin/env python
"""
Script to import data to local PostgreSQL database
Run this after creating local database
"""

import os
import subprocess
import sys
import glob
from datetime import datetime

# Local database credentials (update these as needed)
LOCAL_HOST = "localhost"
LOCAL_DB = "lotusdb"
LOCAL_USER = "postgres"  # or "lotusdb_owner" if you created a specific user
LOCAL_PASSWORD = "your_local_password"  # UPDATE THIS
LOCAL_PORT = "5432"

def find_latest_dump():
    """Find the most recent backup file"""
    dump_files = glob.glob("lotus_neon_backup_*.sql")
    if not dump_files:
        return None
    return max(dump_files, key=os.path.getctime)

def import_database(dump_file):
    """Import the SQL dump to local database"""
    
    # Set environment variable for password
    env = os.environ.copy()
    env['PGPASSWORD'] = LOCAL_PASSWORD
    
    # psql command to import
    cmd = [
        'psql',
        '-h', LOCAL_HOST,
        '-p', LOCAL_PORT,
        '-U', LOCAL_USER,
        '-d', LOCAL_DB,
        '-f', dump_file,
        '--verbose'
    ]
    
    print(f"Importing {dump_file} to local database...")
    print("This may take a few minutes...")
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Import successful!")
            return True
        else:
            print(f"❌ Import failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ psql not found! Please make sure PostgreSQL client tools are installed.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting local database import...")
    
    # Find the latest dump file
    dump_file = find_latest_dump()
    if not dump_file:
        print("❌ No backup file found! Please run export_neon_data.py first.")
        sys.exit(1)
    
    print(f"📁 Found backup file: {dump_file}")
    
    # Update password reminder
    if LOCAL_PASSWORD == "your_local_password":
        print("⚠️  Please update LOCAL_PASSWORD in this script with your actual PostgreSQL password!")
        sys.exit(1)
    
    success = import_database(dump_file)
    
    if success:
        print(f"\n✅ Database import completed successfully!")
        print("\nNext steps:")
        print("1. Update Django settings.py to use local database")
        print("2. Test the connection with: python manage.py migrate")
    else:
        print("\n❌ Import failed. Please check the error messages above.")
