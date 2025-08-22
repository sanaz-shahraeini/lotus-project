#!/usr/bin/env python
"""
Script to fix user authentication issues
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from Alvand.models import Users

def fix_users():
    """Fix user authentication issues"""
    
    print("=" * 60)
    print("LOTUS USER AUTHENTICATION FIX")
    print("=" * 60)
    
    # Fix supporter user password
    supporter = Users.objects.filter(username='supporter').first()
    if supporter:
        print(f"Fixing supporter user password...")
        print(f"Current password: {supporter.password}")
        
        # Set a proper hashed password
        supporter.password = make_password("DLqyS!5#dF13")
        supporter.needs_password_change = False
        supporter.save()
        
        print(f"✅ Supporter password fixed!")
        print(f"New password: DLqyS!5#dF13")
    
    # Fix admin user
    admin = Users.objects.filter(username='admin').first()
    if admin:
        print(f"\nFixing admin user...")
        admin.password = make_password("Admin123!")
        admin.needs_password_change = False
        admin.save()
        
        print(f"✅ Admin password fixed!")
        print(f"New password: Admin123!")
    
    # Fix test user
    test = Users.objects.filter(username='test').first()
    if test:
        print(f"\nFixing test user...")
        test.password = make_password("Test123!")
        test.needs_password_change = False
        test.save()
        
        print(f"✅ Test password fixed!")
        print(f"New password: Test123!")
    
    print("\n" + "=" * 60)
    print("LOGIN CREDENTIALS:")
    print("=" * 60)
    print("Username: supporter")
    print("Password: DLqyS!5#dF13")
    print("\nUsername: admin") 
    print("Password: Admin123!")
    print("\nUsername: test")
    print("Password: Test123!")
    print("=" * 60)

if __name__ == "__main__":
    fix_users()
