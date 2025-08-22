#!/usr/bin/env python
"""
Debug script to test login functionality
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.contrib.auth.hashers import check_password, make_password
from Alvand.models import Users

def debug_login():
    """Debug login functionality"""
    
    print("=" * 60)
    print("LOTUS LOGIN DEBUG TOOL")
    print("=" * 60)
    
    # Get username and password from user
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    print(f"\nTesting login for username: {username}")
    print(f"Password length: {len(password)} characters")
    
    # Check if user exists
    user = Users.objects.filter(username__iexact=username)
    
    if not user.exists():
        print("❌ ERROR: User not found!")
        print(f"No user with username '{username}' exists in database.")
        
        # Show available users
        print("\nAvailable users in database:")
        all_users = Users.objects.all()
        for u in all_users:
            print(f"  - {u.username} (active: {u.active}, group: {u.groupname})")
        return
    
    user_obj = user.first()
    print(f"✅ User found: {user_obj.username}")
    print(f"   Active: {user_obj.active}")
    print(f"   Group: {user_obj.groupname}")
    print(f"   Email: {user_obj.email}")
    print(f"   Stored password hash: {user_obj.password[:50]}...")
    
    # Check if user is active
    if not user_obj.active:
        print("❌ ERROR: User account is not active!")
        return
    
    # Test password
    print(f"\nTesting password...")
    if check_password(password, user_obj.password):
        print("✅ Password is correct!")
        print("✅ Login should succeed!")
    else:
        print("❌ ERROR: Password is incorrect!")
        print(f"   Input password: {password}")
        print(f"   Stored hash: {user_obj.password}")
        
        # Show what the password should hash to
        test_hash = make_password(password)
        print(f"   Test hash for input password: {test_hash}")
        
        # Check if it's a simple password issue
        if password == "12345678":
            print("   Note: You're using the default password '12345678'")
            print("   This might need to be changed first.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    debug_login()
