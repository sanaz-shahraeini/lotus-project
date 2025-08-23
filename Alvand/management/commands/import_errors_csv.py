import os
import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from Alvand.models import Errors


class Command(BaseCommand):
    help = 'Import Errors from a CSV file into the Errors model'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', dest='file', required=True,
                            help='Path to the CSV file (UTF-8 recommended)')
        parser.add_argument('--encoding', dest='encoding', default='utf-8',
                            help='File encoding (default: utf-8)')
        parser.add_argument('--upsert', action='store_true',
                            help='Update existing rows (matched by errorcodenum)')
        parser.add_argument('--dry-run', action='store_true',
                            help='Parse and validate but do not write to DB')

    def handle(self, *args, **options):
        file_path = options['file']
        encoding = options['encoding']
        do_upsert = options['upsert']
        dry_run = options['dry_run']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Reading CSV: {file_path}'))

        # Normalization helper
        def norm(s: str) -> str:
            if s is None:
                return ''
            return (
                str(s).lower().strip()
                .replace('\u200f', '')
                .replace('\u200e', '')
                .replace('\ufeff', '')
                .replace('-', ' ')
                .replace('_', ' ')
            )

        # Header aliases
        aliases = {
            'errorcodenum': {
                'errorcodenum', 'error code', 'error code no', 'error code number', 'error no', 'error number', 'code', 'errcode', 'errorcode'
            },
            'errormessage': {
                'errormessage', 'error message', 'errore message', 'message', 'description', 'error description'
            },
            'probablecause': {
                'probablecause', 'probable cause', 'cause', 'reason'
            },
            'solution': {
                'solution', 'fix', 'resolution', 'action', 'how to fix', 'solutions'
            },
        }

        created, updated, skipped, errors = 0, 0, 0, 0

        # CSV reading (newline='' for proper handling of quoted newlines)
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.reader(f)
                try:
                    headers = next(reader)
                except StopIteration:
                    self.stdout.write(self.style.ERROR('CSV is empty'))
                    return

                # Build column index map
                col_map = {}
                for idx, h in enumerate(headers):
                    key = norm(h)
                    for field, names in aliases.items():
                        if key in names:
                            col_map[field] = idx

                if 'errorcodenum' not in col_map:
                    self.stdout.write(self.style.ERROR(
                        f"Could not locate 'error code' column. Headers detected: {headers}"
                    ))
                    return

                import re

                def parse_code(val):
                    if val is None:
                        return None
                    # Already numeric
                    try:
                        # Handle cases like '000'
                        return int(str(val).strip().split('.')[0])
                    except Exception:
                        pass
                    s = str(val)
                    m = re.search(r'\d+', s)
                    return int(m.group(0)) if m else None

                def get_cell(row, field):
                    idx = col_map.get(field)
                    if idx is None:
                        return ''
                    return row[idx] if idx < len(row) else ''

                with transaction.atomic():
                    for r_idx, row in enumerate(reader, start=2):
                        try:
                            code = parse_code(get_cell(row, 'errorcodenum'))
                            if code is None:
                                skipped += 1
                                continue

                            msg = str(get_cell(row, 'errormessage') or '').strip()
                            cause = str(get_cell(row, 'probablecause') or '').strip()
                            sol = str(get_cell(row, 'solution') or '').strip()

                            if dry_run:
                                continue

                            if do_upsert:
                                obj, was_created = Errors.objects.get_or_create(
                                    errorcodenum=code,
                                    defaults={
                                        'errormessage': msg,
                                        'probablecause': cause,
                                        'solution': sol,
                                    }
                                )
                                if was_created:
                                    created += 1
                                else:
                                    changed = False
                                    if obj.errormessage != msg:
                                        obj.errormessage = msg; changed = True
                                    if obj.probablecause != cause:
                                        obj.probablecause = cause; changed = True
                                    if obj.solution != sol:
                                        obj.solution = sol; changed = True
                                    if changed:
                                        obj.save(update_fields=['errormessage', 'probablecause', 'solution', 'updated_at'])
                                        updated += 1
                            else:
                                if Errors.objects.filter(errorcodenum=code).exists():
                                    skipped += 1
                                else:
                                    Errors.objects.create(
                                        errorcodenum=code,
                                        errormessage=msg,
                                        probablecause=cause,
                                        solution=sol,
                                    )
                                    created += 1
                        except Exception as e:
                            errors += 1
                            self.stdout.write(self.style.WARNING(f'Row {r_idx}: {e}'))

        except UnicodeDecodeError:
            self.stdout.write(self.style.ERROR(
                f'Encoding error. Try specifying --encoding (current: {encoding})'
            ))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to read CSV: {e}'))
            return

        if dry_run:
            self.stdout.write(self.style.SUCCESS('Dry-run completed successfully.'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Import summary:'))
        self.stdout.write(f'  Created: {created}')
        self.stdout.write(f'  Updated: {updated}')
        self.stdout.write(f'  Skipped: {skipped}')
        self.stdout.write(f'  Errors:  {errors}')
