import sys
import os
from django.core.management.base import BaseCommand
from Alvand.models import Records
import datetime
import importlib.util

class Command(BaseCommand):
    help = 'Import call records from records.py file into the Records database model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force import without confirmation',
        )

    def handle(self, *args, **options):
        try:
            # Get the absolute path to records.py
            records_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'records.py')
            
            if not os.path.exists(records_path):
                self.stdout.write(self.style.ERROR(f'Could not find records.py at {records_path}'))
                return
                
            # Load the records.py file as a module
            spec = importlib.util.spec_from_file_location("records_module", records_path)
            records_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(records_module)
            
            # Check if records list exists in the module
            if not hasattr(records_module, 'records'):
                self.stdout.write(self.style.ERROR('No "records" variable found in records.py'))
                return
                
            # Get the records from the module
            records_data = records_module.records
            
            # Get current records count
            current_count = Records.objects.count()
            if current_count > 0:
                if options['force']:
                    # Auto confirm if --force flag is used
                    confirm = 'y'
                else:
                    self.stdout.write(f'There are already {current_count} records in the database.')
                    confirm = input('Do you want to clear existing records and import new ones? (y/n): ')
                
                if confirm.lower() != 'y':
                    self.stdout.write('Import aborted.')
                    return
                
                Records.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted {current_count} existing records.'))
            
            # Import the records
            imported_count = 0
            total_records = len(records_data)
            
            self.stdout.write(f'Starting import of {total_records} records...')
            
            batch_size = 1000
            batches = []
            
            for record_data in records_data:
                # Unpack the record tuple into the right field names
                rec_id, rec_date, rec_time, frm, ext, to, cal_type, cal_time, transfer_to, call_price, transfer, rec_created, rec_updated = record_data
                
                # Make sure contact number is not empty
                contact_number = to if to else ""
                
                # Remove any leading zeros from phone numbers for consistency
                if contact_number and contact_number.startswith('00'):
                    contact_number = '+' + contact_number[2:]
                
                # Create a Records instance without saving it yet
                record = Records(
                    date=rec_date,
                    hour=rec_time,
                    extension=frm,
                    urbanline=ext,
                    contactnumber=contact_number,
                    calltype=cal_type,
                    durationtime=cal_time,
                    internal=transfer_to,
                    beepsnumber=call_price,
                    transferring=transfer,
                    created_at=rec_created or datetime.datetime.now(datetime.timezone.utc),
                    updated_at=rec_updated
                )
                batches.append(record)
                
                # When we reach batch_size, bulk create
                if len(batches) >= batch_size:
                    Records.objects.bulk_create(batches)
                    imported_count += len(batches)
                    self.stdout.write(f'Imported {imported_count}/{total_records} records ({(imported_count/total_records)*100:.1f}%)...')
                    batches = []
            
            # Create any remaining records
            if batches:
                Records.objects.bulk_create(batches)
                imported_count += len(batches)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {imported_count} records from records.py'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing records: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc())) 