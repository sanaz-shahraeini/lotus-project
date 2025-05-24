import os
import re
import datetime
from django.core.management.base import BaseCommand
from Alvand.models import SMDRRecord

class Command(BaseCommand):
    help = 'Import SMDR records from a text file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the SMDR report file'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force import without confirmation'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        force = options['force']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
            
        # Check if records already exist
        record_count = SMDRRecord.objects.count()
        if record_count > 0:
            if force:
                confirm = 'y'
            else:
                self.stdout.write(f'There are already {record_count} SMDR records in the database.')
                confirm = input('Do you want to clear existing records and import new ones? (y/n): ')
                
            if confirm.lower() != 'y':
                self.stdout.write('Import aborted.')
                return
                
            SMDRRecord.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {record_count} existing records.'))
        
        # Process the file
        imported_count = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                # Find header lines
                header_indexes = []
                for i, line in enumerate(lines):
                    if 'Date' in line and 'Time' in line and 'Ext' in line and 'CO' in line and 'Duration' in line:
                        header_indexes.append(i)
                    if '-' * 10 in line:  # Separator line
                        header_indexes.append(i)
                
                total_lines = len(lines)
                batch_size = 100
                records_to_create = []
                
                # Process lines
                for i, line in enumerate(lines):
                    # Skip headers and separators
                    if i in header_indexes or re.match(r'^-+$', line.strip()) or not line.strip():
                        continue
                    
                    # Check if line is a system message (MN ALM)
                    is_system_msg = 'MN ALM' in line
                    
                    # Parse normal call record
                    if not is_system_msg and len(line.strip()) > 20:
                        try:
                            # Splitting based on fixed width or delimiters
                            parts = line.strip().split()
                            
                            if len(parts) >= 6:
                                # Extract date and time
                                date_str = parts[0] if '/' in parts[0] else None
                                time_str = parts[1] if ':' in parts[1] else None
                                
                                if date_str and time_str:
                                    # Parse date (assuming DD/MM/YY format)
                                    date_parts = date_str.split('/')
                                    if len(date_parts) == 3:
                                        day, month, year = map(int, date_parts)
                                        # Assuming 20xx for years written as YY
                                        if year < 100:
                                            year += 2000
                                        date_obj = datetime.date(year, month, day)
                                    else:
                                        date_obj = None
                                    
                                    # Parse time
                                    time_parts = time_str.split(':')
                                    if len(time_parts) == 2:
                                        hour, minute = map(int, time_parts)
                                        time_obj = datetime.time(hour, minute)
                                    else:
                                        time_obj = None
                                    
                                    # Extract other fields
                                    ext = parts[2] if len(parts) > 2 else None
                                    co = parts[3] if len(parts) > 3 else None
                                    
                                    # Extract dial number - it might contain spaces, so joining remaining parts
                                    dial_number = None
                                    ring_time = None
                                    duration = None
                                    acc_code = None
                                    cd_code = None
                                    
                                    # Try to identify fields based on patterns
                                    dial_index = 4
                                    if len(parts) > dial_index:
                                        # Check if it's a number or special case like <I>
                                        dial_number = parts[dial_index]
                                        
                                        # Look for duration which often has format like 00:00'45
                                        for i, part in enumerate(parts[dial_index+1:], dial_index+1):
                                            if "'" in part or ":" in part:
                                                if not duration:  # Only set duration once
                                                    duration = part
                                                    break
                                        
                                        # Look for other fields
                                        for i, part in enumerate(parts):
                                            if i > dial_index:
                                                # Check for CD code at the end
                                                if i == len(parts) - 1 and len(part) <= 2:
                                                    cd_code = part
                                                # Check for acc_code
                                                elif 6 <= len(part) <= 12 and i > 5:
                                                    acc_code = part
                                    
                                    # Determine call type
                                    call_type = "Unknown"
                                    is_incoming = False
                                    is_outgoing = False
                                    is_internal = False
                                    
                                    # Incoming calls often have <I> in dial number
                                    if dial_number and '<I>' in dial_number:
                                        call_type = "Incoming"
                                        is_incoming = True
                                    # EXT in dial number usually means internal call
                                    elif dial_number and 'EXT' in dial_number:
                                        call_type = "Internal"
                                        is_internal = True
                                    # If CO has a value and dial_number has a value (not starting with EXT), likely outgoing
                                    elif co and dial_number and not dial_number.startswith('EXT'):
                                        call_type = "Outgoing"
                                        is_outgoing = True
                                    
                                    # Create SMDRRecord object
                                    record = SMDRRecord(
                                        date=date_obj,
                                        time=time_obj,
                                        ext=ext,
                                        co=co,
                                        dial_number=dial_number,
                                        ring_time=ring_time,
                                        duration=duration,
                                        acc_code=acc_code,
                                        cd_code=cd_code,
                                        call_type=call_type,
                                        is_incoming=is_incoming,
                                        is_outgoing=is_outgoing,
                                        is_internal=is_internal,
                                        is_system_message=False
                                    )
                                    records_to_create.append(record)
                            
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'Error parsing line {i+1}: {str(e)}'))
                    
                    # Parse system message
                    elif is_system_msg:
                        try:
                            # Parse date time
                            parts = line.strip().split()
                            if len(parts) >= 3:
                                date_str = parts[0] if '/' in parts[0] else None
                                time_str = parts[1] if ':' in parts[1] else None
                                
                                if date_str and time_str:
                                    # Parse date
                                    date_parts = date_str.split('/')
                                    if len(date_parts) == 3:
                                        day, month, year = map(int, date_parts)
                                        if year < 100:
                                            year += 2000
                                        date_obj = datetime.date(year, month, day)
                                    else:
                                        date_obj = None
                                    
                                    # Parse time
                                    time_parts = time_str.split(':')
                                    if len(time_parts) == 2:
                                        hour, minute = map(int, time_parts)
                                        time_obj = datetime.time(hour, minute)
                                    else:
                                        time_obj = None
                                    
                                    # Extract system message
                                    message_parts = parts[2:]
                                    message = ' '.join(message_parts)
                                    
                                    # Create system message record
                                    record = SMDRRecord(
                                        date=date_obj,
                                        time=time_obj,
                                        dial_number=message,
                                        call_type="System",
                                        is_system_message=True
                                    )
                                    records_to_create.append(record)
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'Error parsing system message line {i+1}: {str(e)}'))
                    
                    # Batch create records
                    if len(records_to_create) >= batch_size:
                        SMDRRecord.objects.bulk_create(records_to_create)
                        imported_count += len(records_to_create)
                        self.stdout.write(f'Imported {imported_count} records...')
                        records_to_create = []
                
                # Create remaining records
                if records_to_create:
                    SMDRRecord.objects.bulk_create(records_to_create)
                    imported_count += len(records_to_create)
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {imported_count} SMDR records.'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing records: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc())) 