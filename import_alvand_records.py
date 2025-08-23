#!/usr/bin/env python
"""
Specialized script to import Alvand_records.csv into PostgreSQL
This script maps the CSV fields to the Records model correctly
"""

import os
import sys
import csv
import django
from datetime import datetime
from pathlib import Path

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.db import transaction
from Alvand.models import Records

def parse_date(date_str):
    """Parse date string to date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None

def parse_time(time_str):
    """Parse time string to time object"""
    if not time_str:
        return None
    try:
        return datetime.strptime(time_str, '%H:%M:%S').time()
    except:
        return None

def parse_datetime(datetime_str):
    """Parse datetime string to datetime object"""
    if not datetime_str:
        return None
    try:
        # Handle timezone info if present
        if '+' in datetime_str:
            datetime_str = datetime_str.split('+')[0]
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
    except:
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except:
            return None

def parse_transferring(transferring_str):
    """Parse transferring field which might be a JSON array"""
    if not transferring_str:
        return None
    try:
        # Remove quotes and brackets, split by comma
        cleaned = transferring_str.strip('[]"').replace('"', '')
        if cleaned:
            return [item.strip() for item in cleaned.split(',') if item.strip()]
        return None
    except:
        return None

def import_alvand_records(csv_file_path):
    """Import Alvand_records.csv into the Records table"""
    print(f"🔄 Starting import of {csv_file_path}")
    
    if not os.path.exists(csv_file_path):
        print(f"❌ File not found: {csv_file_path}")
        return False
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            print(f"📋 CSV columns: {list(reader.fieldnames)}")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    with transaction.atomic():
                        # Map CSV fields to model fields
                        record_data = {
                            'date': parse_date(row.get('date')),
                            'hour': parse_time(row.get('hour')),
                            'extension': row.get('extension', ''),
                            'urbanline': row.get('urbanline', ''),
                            'contactnumber': row.get('contactnumber', ''),
                            'calltype': row.get('calltype', ''),
                            'durationtime': row.get('durationtime', ''),
                            'internal': row.get('internal') if row.get('internal') else None,
                            'beepsnumber': row.get('beepsnumber', ''),
                            'transferring': parse_transferring(row.get('transferring')),
                            'created_at': parse_datetime(row.get('created_at')),
                            'updated_at': parse_datetime(row.get('updated_at'))
                        }
                        
                        # Create the record
                        Records.objects.create(**record_data)
                        success_count += 1
                        
                        if success_count % 100 == 0:
                            print(f"⏳ Processed {success_count} records...")
                        
                except Exception as e:
                    error_count += 1
                    print(f"❌ Row {row_num}: Error - {str(e)}")
                    print(f"   Data: {row}")
                    continue
    
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Print summary
    print(f"\n📊 Import Summary:")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"⚠️  Skipped: {skipped_count}")
    print(f"📈 Total: {success_count + error_count + skipped_count}")
    
    return True

def main():
    """Main function"""
    csv_file = "Alvand_records.csv"
    
    print("🚀 Alvand Records CSV Import Tool")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        print("Please make sure Alvand_records.csv is in the current directory")
        return
    
    # Confirm with user
    print(f"📁 Found CSV file: {csv_file}")
    print("This will import records into the PostgreSQL database.")
    
    try:
        # Count existing records
        existing_count = Records.objects.count()
        print(f"📊 Current records in database: {existing_count}")
        
        # Import records
        success = import_alvand_records(csv_file)
        
        if success:
            new_count = Records.objects.count()
            print(f"\n🎉 Import completed successfully!")
            print(f"📈 Records in database: {new_count} (added {new_count - existing_count})")
        else:
            print("\n❌ Import failed. Check error messages above.")
            
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

