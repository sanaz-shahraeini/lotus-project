#!/usr/bin/env python
"""
Script to create the Records table directly using SQL
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

def create_records_table():
    """Create the Records table directly using SQL"""
    
    print("=" * 60)
    print("CREATING RECORDS TABLE")
    print("=" * 60)
    
    # SQL to create the Records table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS alvand_records (
        id SERIAL PRIMARY KEY,
        date DATE,
        hour TIME,
        extension VARCHAR(200),
        urbanline VARCHAR(200),
        contactnumber VARCHAR(200),
        calltype VARCHAR(200) NOT NULL,
        durationtime VARCHAR(200),
        internal BIGINT,
        beepsnumber VARCHAR(200),
        transferring TEXT[],
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE
    );
    """
    
    try:
        with connection.cursor() as cursor:
            print("Creating alvand_records table...")
            cursor.execute(create_table_sql)
            print("✅ Table created successfully!")
            
            # Check if table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'alvand_records'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if table_exists:
                print("✅ Table verification successful!")
                
                # Count records
                cursor.execute("SELECT COUNT(*) FROM alvand_records;")
                count = cursor.fetchone()[0]
                print(f"📊 Current record count: {count}")
                
            else:
                print("❌ Table creation failed!")
                
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_records_table()
