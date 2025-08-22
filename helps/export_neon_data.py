#!/usr/bin/env python
"""
Script to export data from Neon PostgreSQL database
Run this before switching to local database
"""

import os
import subprocess
import sys
from datetime import datetime

# Neon database credentials
NEON_HOST = "ep-orange-mud-a2by6urk-pooler.eu-central-1.aws.neon.tech"
NEON_DB = "lotusdb"
NEON_USER = "lotusdb_owner"
NEON_PASSWORD = "npg_6dUorONf5mtR"
NEON_PORT = "5432"

def export_database():
    """Export the Neon database to a SQL dump file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_file = f"lotus_neon_backup_{timestamp}.sql"
    
    # Set environment variable for password
    env = os.environ.copy()
    env['PGPASSWORD'] = NEON_PASSWORD
    
    # pg_dump command
    cmd = [
        'pg_dump',
        '-h', NEON_HOST,
        '-p', NEON_PORT,
        '-U', NEON_USER,
        '-d', NEON_DB,
        '--verbose',
        '--no-owner',
        '--no-privileges',
        '-f', dump_file
    ]
    
    print(f"Exporting Neon database to {dump_file}...")
    print("This may take a few minutes...")
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Export successful! Database exported to: {dump_file}")
            print(f"File size: {os.path.getsize(dump_file) / 1024 / 1024:.2f} MB")
            return dump_file
        else:
            print(f"❌ Export failed!")
            print(f"Error: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ pg_dump not found! Please make sure PostgreSQL client tools are installed.")
        print("You can install them from: https://www.postgresql.org/download/windows/")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Starting Neon database export...")
    dump_file = export_database()
    
    if dump_file:
        print(f"\n📁 Backup file created: {dump_file}")
        print("\nNext steps:")
        print("1. Install PostgreSQL locally")
        print("2. Create local database")
        print("3. Run: python import_to_local.py")
    else:
        print("\n❌ Export failed. Please check the error messages above.")
