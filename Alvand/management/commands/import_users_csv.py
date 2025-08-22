import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from Alvand.models import Users, Groups, Infos, Permissions
from django.utils import timezone


class Command(BaseCommand):
    help = 'Import users from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing users instead of creating new ones'
        )
        parser.add_argument(
            '--skip-errors',
            action='store_true',
            help='Skip rows with errors and continue processing'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        update_existing = options['update']
        skip_errors = options['skip_errors']

        if not os.path.exists(csv_file):
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_file}')
            )
            return

        # Get or create default group if needed
        default_group, created = Groups.objects.get_or_create(
            pename='کاربران پیش‌فرض',
            enname='Default Users',
            defaults={'active': True}
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created default group: {default_group.pename}')
            )

        success_count = 0
        error_count = 0
        skipped_count = 0

        with open(csv_file, 'r', encoding='utf-8') as file:
            # Try to detect the delimiter
            sample = file.read(1024)
            file.seek(0)
            
            # Common delimiters to try
            delimiters = [',', ';', '\t', '|']
            detected_delimiter = ','
            
            for delimiter in delimiters:
                if delimiter in sample:
                    detected_delimiter = delimiter
                    break

            self.stdout.write(f'Detected delimiter: "{detected_delimiter}"')
            
            reader = csv.DictReader(file, delimiter=detected_delimiter)
            
            # Show CSV headers for debugging
            self.stdout.write(f'CSV Headers: {list(reader.fieldnames)}')
            
            for row_num, row in enumerate(reader, start=2):  # Start from 2 since row 1 is headers
                try:
                    with transaction.atomic():
                        # Handle required fields with defaults
                        username = row.get('username', '').strip()
                        if not username:
                            if skip_errors:
                                self.stdout.write(
                                    self.style.WARNING(f'Row {row_num}: Skipping - no username')
                                )
                                skipped_count += 1
                                continue
                            else:
                                raise ValueError(f'Row {row_num}: Username is required')

                        # Check if user exists
                        user_exists = Users.objects.filter(username=username).exists()
                        
                        if user_exists and not update_existing:
                            if skip_errors:
                                self.stdout.write(
                                    self.style.WARNING(f'Row {row_num}: Skipping - user {username} already exists')
                                )
                                skipped_count += 1
                                continue
                            else:
                                raise ValueError(f'Row {row_num}: User {username} already exists')

                        # Prepare user data
                        user_data = {
                            'active': self._parse_boolean(row.get('active', 'true')),
                            'online': int(row.get('online', 1)),
                            'extension': int(row.get('extension', 0)) if row.get('extension') else 0,
                            'name': row.get('name', '').strip() or username,
                            'username': username,
                            'lastname': row.get('lastname', '').strip() or '',
                            'group': default_group,
                            'groupname': default_group.pename,
                            'picurl': row.get('picurl', 'avatar.png'),
                            'profile_picture': row.get('profile_picture', ''),
                            'email': row.get('email', '').strip() or '',
                            'password': make_password(row.get('password', 'defaultpassword123')),
                            'needs_password_change': self._parse_boolean(row.get('needs_password_change', 'true')),
                        }

                        # Handle usersextension array field
                        if row.get('usersextension'):
                            extensions = [ext.strip() for ext in str(row['usersextension']).split(',') if ext.strip()]
                            user_data['usersextension'] = extensions

                        if user_exists and update_existing:
                            # Update existing user
                            Users.objects.filter(username=username).update(**user_data)
                            user = Users.objects.get(username=username)
                            self.stdout.write(
                                self.style.SUCCESS(f'Row {row_num}: Updated user {username}')
                            )
                        else:
                            # Create new user
                            user = Users.objects.create(**user_data)
                            self.stdout.write(
                                self.style.SUCCESS(f'Row {row_num}: Created user {username}')
                            )

                        # Create or update Infos model
                        infos_data = {
                            'user': user,
                            'birthdate': row.get('birthdate', ''),
                            'phonenumber': row.get('phonenumber', ''),
                            'telephone': row.get('telephone', ''),
                            'province': row.get('province', ''),
                            'city': row.get('city', ''),
                            'address': row.get('address', ''),
                            'gender': self._parse_choice(row.get('gender'), ['0', '1', '2']),
                            'military': self._parse_choice(row.get('military'), ['0', '1', '2', '3', '4']),
                            'maritalstatus': self._parse_choice(row.get('maritalstatus'), ['0', '1']),
                            'educationdegree': self._parse_choice(row.get('educationdegree'), ['0', '1', '2', '3', '4', '5', '6']),
                            'educationfield': row.get('educationfield', ''),
                            'cardnumber': row.get('cardnumber', ''),
                            'accountnumber': row.get('accountnumber', ''),
                            'accountnumbershaba': row.get('accountnumbershaba', ''),
                            'macaddress': row.get('macaddress', ''),
                            'nationalcode': int(row.get('nationalcode', 0)) if row.get('nationalcode') else None,
                            'groupname': row.get('groupname', ''),
                        }

                        Infos.objects.update_or_create(
                            user=user,
                            defaults=infos_data
                        )

                        # Create or update Permissions model
                        permissions_data = {
                            'user': user,
                            'perm_email': self._parse_boolean(row.get('perm_email', 'false')),
                            'can_view': self._parse_boolean(row.get('can_view', 'false')),
                            'can_write': self._parse_boolean(row.get('can_write', 'false')),
                            'can_delete': self._parse_boolean(row.get('can_delete', 'false')),
                            'can_modify': self._parse_boolean(row.get('can_modify', 'false')),
                            'errorsreport': self._parse_boolean(row.get('errorsreport', 'false')),
                        }

                        # Handle exts_label array field
                        if row.get('exts_label'):
                            exts = [ext.strip() for ext in str(row['exts_label']).split(',') if ext.strip()]
                            permissions_data['exts_label'] = exts

                        Permissions.objects.update_or_create(
                            user=user,
                            defaults=permissions_data
                        )

                        success_count += 1

                except Exception as e:
                    error_count += 1
                    error_msg = f'Row {row_num}: Error - {str(e)}'
                    self.stdout.write(self.style.ERROR(error_msg))
                    
                    if not skip_errors:
                        raise e

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write('IMPORT SUMMARY')
        self.stdout.write('='*50)
        self.stdout.write(f'Successfully processed: {success_count}')
        self.stdout.write(f'Errors: {error_count}')
        self.stdout.write(f'Skipped: {skipped_count}')
        self.stdout.write('='*50)

    def _parse_boolean(self, value):
        """Parse boolean values from CSV"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            value = value.lower().strip()
            return value in ['true', '1', 'yes', 'y', 'on']
        return bool(value)

    def _parse_choice(self, value, choices):
        """Parse choice values from CSV"""
        if not value:
            return None
        value = str(value).strip()
        if value in choices:
            return value
        return None

