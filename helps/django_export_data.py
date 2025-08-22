#!/usr/bin/env python
"""
Django-based data export script (alternative to pg_dump)
This exports data using Django ORM instead of pg_dump
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.core import serializers
from django.apps import apps
from django.db import connection

def export_all_data():
    """Export all data from all models to JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = f"lotus_data_export_{timestamp}.json"
    
    print("🚀 Starting Django-based data export...")
    
    # Get all models from your app
    all_models = []
    for app_config in apps.get_app_configs():
        if app_config.name == 'Alvand':  # Your main app
            all_models.extend(app_config.get_models())
    
    # Export data
    all_data = []
    total_objects = 0
    
    for model in all_models:
        model_name = f"{model._meta.app_label}.{model._meta.model_name}"
        objects = model.objects.all()
        count = objects.count()
        
        if count > 0:
            print(f"📊 Exporting {count} objects from {model_name}")
            serialized = serializers.serialize('json', objects)
            all_data.extend(json.loads(serialized))
            total_objects += count
        else:
            print(f"⚪ No data in {model_name}")
    
    # Save to file
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    file_size = os.path.getsize(export_file) / 1024 / 1024
    print(f"\n✅ Export completed!")
    print(f"📁 File: {export_file}")
    print(f"📊 Total objects: {total_objects}")
    print(f"💾 File size: {file_size:.2f} MB")
    
    return export_file

def export_schema():
    """Export database schema information"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    schema_file = f"lotus_schema_{timestamp}.sql"
    
    print("📋 Exporting database schema...")
    
    with connection.cursor() as cursor:
        # Get all table creation statements
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        with open(schema_file, 'w') as f:
            f.write("-- Database Schema Export\n")
            f.write(f"-- Generated on {datetime.now()}\n\n")
            
            for (table_name,) in tables:
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """)
                
                columns = cursor.fetchall()
                f.write(f"-- Table: {table_name}\n")
                for col in columns:
                    f.write(f"-- {col[0]}: {col[1]} {'NULL' if col[2] == 'YES' else 'NOT NULL'}\n")
                f.write("\n")
    
    print(f"✅ Schema exported to: {schema_file}")
    return schema_file

if __name__ == "__main__":
    try:
        # Export data
        data_file = export_all_data()
        
        # Export schema
        schema_file = export_schema()
        
        print(f"\n🎉 Export completed successfully!")
        print(f"📁 Data file: {data_file}")
        print(f"📁 Schema file: {schema_file}")
        print("\nNext steps:")
        print("1. Install PostgreSQL locally")
        print("2. Create local database")
        print("3. Update settings.py")
        print("4. Run: python manage.py migrate")
        print("5. Run: python django_import_data.py")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
