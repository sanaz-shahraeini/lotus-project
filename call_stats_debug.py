import os
import django
import sys

# Add the project root to the path
sys.path.append('d:\\lotus1')

# Try to detect the correct settings module
settings_candidates = ['settings', 'lotus.settings', 'lotus1.settings']
settings_found = False

for settings_module in settings_candidates:
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        django.setup()
        settings_found = True
        print(f"Successfully loaded settings module: {settings_module}")
        break
    except Exception as e:
        print(f"Failed to load {settings_module}: {e}")

if not settings_found:
    print("Could not find the correct settings module. Let's try another approach:")
    
    # List all Python files in the root directory to find potential settings files
    root_files = os.listdir('d:\\lotus1')
    python_files = [f for f in root_files if f.endswith('.py')]
    print(f"Python files in root directory: {python_files}")
    
    # Try to identify Django settings files
    for file in python_files:
        with open(os.path.join('d:\\lotus1', file), 'r', encoding='utf-8', errors='ignore') as f:
            try:
                content = f.read()
                if 'DATABASES' in content or 'INSTALLED_APPS' in content:
                    print(f"Potential Django settings file found: {file}")
            except Exception as e:
                print(f"Error reading {file}: {e}")

# Import models
from Alvand.models import Records

# Print total count
total_count = Records.objects.count()
print(f"Total records in database: {total_count}")

# Get unique call types
unique_call_types = list(Records.objects.values_list('calltype', flat=True).distinct())
print(f"Unique call types: {unique_call_types}")

# Count each call type
for call_type in unique_call_types:
    count = Records.objects.filter(calltype=call_type).count()
    print(f"Call type '{call_type}': {count} records")

# Check the first few records to see what they look like
print("\nSample records:")
for record in Records.objects.all()[:5]:
    print(f"ID: {record.id}, Date: {record.date}, Call Type: {record.calltype}, Extension: {record.extension}")

# Check if there are any records with missing call type
null_calltype = Records.objects.filter(calltype__isnull=True).count()
print(f"\nRecords with NULL calltype: {null_calltype}")

# Check if any records have empty string as call type
empty_calltype = Records.objects.filter(calltype="").count()
print(f"Records with empty calltype: {empty_calltype}")
