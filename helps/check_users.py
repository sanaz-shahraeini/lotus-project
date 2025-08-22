#!/usr/bin/env python
"""
Script to check users in the database
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from Alvand.models import Users

def check_users():
    """Check all users in the database"""
    
    print("=" * 60)
    print("LOTUS DATABASE USERS")
    print("=" * 60)
    
    users = Users.objects.all()
    
    if not users.exists():
        print("❌ No users found in database!")
        return
    
    print(f"Found {users.count()} user(s) in database:\n")
    
    for i, user in enumerate(users, 1):
        print(f"{i}. Username: {user.username}")
        print(f"   Name: {user.name} {user.lastname}")
        print(f"   Email: {user.email}")
        print(f"   Active: {user.active}")
        print(f"   Group: {user.groupname}")
        print(f"   Extension: {user.extension}")
        print(f"   Password hash: {user.password[:30]}...")
        print(f"   Needs password change: {user.needs_password_change}")
        print(f"   Created: {user.created_at}")
        print("-" * 40)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_users()
