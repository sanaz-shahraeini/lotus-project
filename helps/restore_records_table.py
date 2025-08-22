#!/usr/bin/env python
"""
Script to restore the Alvand_records table and import data from CSV
"""

import os
import sys
import django
import csv
from datetime import datetime, time

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from Alvand.models import Records

def restore_records_table():
    """Restore the Records table and import data from CSV"""
    
    print("=" * 60)
    print("LOTUS RECORDS TABLE RESTORATION")
    print("=" * 60)
    
    # Step 1: Check if table exists
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'alvand_records'
            );
        """)
        table_exists = cursor.fetchone()[0]
    
    if table_exists:
        print("✅ Records table already exists!")
        print("Checking if it has data...")
        
        record_count = Records.objects.count()
        print(f"Current record count: {record_count}")
        
        if record_count > 0:
            print("Table has data. Do you want to:")
            print("1. Keep existing data")
            print("2. Clear and reimport from CSV")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                print("Keeping existing data. Exiting...")
                return
            elif choice == "2":
                print("Clearing existing data...")
                Records.objects.all().delete()
                print("✅ Existing data cleared.")
            elif choice == "3":
                print("Exiting...")
                return
            else:
                print("Invalid choice. Exiting...")
                return
    else:
        print("❌ Records table does not exist. Creating it...")
        
        # Create the table using Django migrations
        try:
            print("Running migrations to create the table...")
            execute_from_command_line(['manage.py', 'makemigrations'])
            execute_from_command_line(['manage.py', 'migrate'])
            print("✅ Table created successfully!")
        except Exception as e:
            print(f"❌ Error creating table: {e}")
            return
    
    # Step 2: Import data from CSV
    csv_file = "Alvand_records.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file '{csv_file}' not found!")
        return
    
    print(f"\n📁 Found CSV file: {csv_file}")
    print("Starting data import...")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            records_to_create = []
            total_rows = 0
            imported_count = 0
            
            # First, count total rows
            file.seek(0)
            next(reader)  # Skip header
            total_rows = sum(1 for row in reader)
            
            print(f"Total rows to import: {total_rows}")
            
            # Reset file pointer
            file.seek(0)
            next(reader)  # Skip header again
            
            for row_num, row in enumerate(reader, 1):
                try:
                    # Parse date
                    date_str = row.get('date', '').strip()
                    if date_str:
                        try:
                            # Try different date formats
                            if '/' in date_str:
                                date_obj = datetime.strptime(date_str, '%Y/%m/%d').date()
                            else:
                                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            print(f"⚠️  Warning: Invalid date format in row {row_num}: {date_str}")
                            date_obj = None
                    else:
                        date_obj = None
                    
                    # Parse time
                    time_str = row.get('hour', '').strip()
                    if time_str:
                        try:
                            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
                        except ValueError:
                            print(f"⚠️  Warning: Invalid time format in row {row_num}: {time_str}")
                            time_obj = None
                    else:
                        time_obj = None
                    
                    # Create record object
                    record = Records(
                        date=date_obj,
                        hour=time_obj,
                        extension=row.get('extension', '').strip() or None,
                        urbanline=row.get('urbanline', '').strip() or None,
                        contactnumber=row.get('contactnumber', '').strip() or None,
                        calltype=row.get('calltype', '').strip() or '',
                        durationtime=row.get('durationtime', '').strip() or None,
                        internal=row.get('internal', '').strip() or None,
                        beepsnumber=row.get('beepsnumber', '').strip() or None,
                        transferring=row.get('transferring', '').strip() or None,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    
                    records_to_create.append(record)
                    imported_count += 1
                    
                    # Show progress every 100 records
                    if imported_count % 100 == 0:
                        print(f"📊 Processed {imported_count}/{total_rows} records...")
                    
                    # Batch insert every 1000 records
                    if len(records_to_create) >= 1000:
                        Records.objects.bulk_create(records_to_create, ignore_conflicts=True)
                        records_to_create = []
                        print(f"💾 Saved batch of 1000 records...")
                
                except Exception as e:
                    print(f"❌ Error processing row {row_num}: {e}")
                    print(f"   Row data: {row}")
                    continue
            
            # Insert remaining records
            if records_to_create:
                Records.objects.bulk_create(records_to_create, ignore_conflicts=True)
                print(f"💾 Saved final batch of {len(records_to_create)} records...")
            
            print(f"\n✅ Import completed!")
            print(f"📊 Total records imported: {imported_count}")
            
            # Verify import
            final_count = Records.objects.count()
            print(f"📊 Final record count in database: {final_count}")
            
    except Exception as e:
        print(f"❌ Error importing data: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🎉 RECORDS TABLE RESTORATION COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    restore_records_table()
