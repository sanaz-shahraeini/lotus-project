from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from Alvand.models import (
    Connections, Costs, Countries, Device, Emailsending, Errors,
    Extensionsgroups, Faults, Groups, Infos, Permissions, Records,
    Telephons, Users, Verifications, PasswordResetRequest, Log,
    ContactInfo, errorsSent, lices, SMDRRecord
)
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Delete all rows from all tables in LotusDB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data',
        )
        parser.add_argument(
            '--tables',
            nargs='+',
            type=str,
            help='Specific tables to clear (space-separated list)',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'WARNING: This will delete ALL data from ALL tables in LotusDB!\n'
                    'This action cannot be undone.\n'
                    'Use --confirm flag to proceed.'
                )
            )
            return

        # Get all models from the Alvand app
        models_to_clear = [
            Connections, Costs, Countries, Device, Emailsending, Errors,
            Extensionsgroups, Faults, Groups, Infos, Permissions, Records,
            Telephons, Users, Verifications, PasswordResetRequest, Log,
            ContactInfo, errorsSent, lices, SMDRRecord
        ]

        # Filter by specific tables if provided
        if options['tables']:
            table_names = [name.lower() for name in options['tables']]
            models_to_clear = [
                model for model in models_to_clear 
                if model._meta.db_table.lower() in table_names
            ]
            self.stdout.write(f"Clearing only specified tables: {options['tables']}")

        # Disable foreign key checks temporarily (PostgreSQL specific)
        with connection.cursor() as cursor:
            cursor.execute("SET session_replication_role = replica;")

        try:
            total_deleted = 0
            
            for model in models_to_clear:
                try:
                    count = model.objects.count()
                    if count > 0:
                        model.objects.all().delete()
                        total_deleted += count
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✓ Deleted {count} rows from {model._meta.db_table}"
                            )
                        )
                    else:
                        self.stdout.write(
                            f"  No data in {model._meta.db_table}"
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"✗ Error clearing {model._meta.db_table}: {str(e)}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n🎉 Successfully deleted {total_deleted} total rows from all tables!"
                )
            )

        finally:
            # Re-enable foreign key checks
            with connection.cursor() as cursor:
                cursor.execute("SET session_replication_role = DEFAULT;")

        self.stdout.write(
            self.style.SUCCESS(
                "\n✅ Database clearing completed successfully!"
            )
        )
