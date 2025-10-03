"""
Script to create a test password reset request
Run this with: python manage.py shell < create_test_reset_request.py
"""

from Alvand.models import Users, PasswordResetRequest

# Find a test user (not supporter)
test_user = Users.objects.filter(groupname='member').first()

if not test_user:
    # Try to find any user that's not supporter
    test_user = Users.objects.exclude(groupname='supporter').first()

if test_user:
    # Create a password reset request
    request = PasswordResetRequest.objects.create(user=test_user)
    print(f"✅ Password reset request created successfully!")
    print(f"   User: {test_user.username}")
    print(f"   Name: {test_user.name} {test_user.lastname}")
    print(f"   Request ID: {request.id}")
    print(f"   Created at: {request.created_at}")
else:
    print("❌ No suitable user found to create a test request")
    print("   Please create a user first with groupname='member'")
