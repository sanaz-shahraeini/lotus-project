import os
import sys
import django
import traceback
import time

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from Alvand.models import Users, Groups, Permissions, Infos
from django.contrib.auth.hashers import make_password

def debug_user_creation():
    print("=" * 50)
    print("USER CREATION DEBUGGING")
    print("=" * 50)
    
    # Get total users before
    user_count_before = Users.objects.count()
    print(f"Users before: {user_count_before}")
    
    # Get a group
    try:
        group = Groups.objects.first()
        if not group:
            print("ERROR: No groups found in database!")
            return
        print(f"Using group: {group.id} - {group.pename} ({group.enname})")
    except Exception as e:
        print(f"ERROR getting group: {e}")
        traceback.print_exc()
        return
    
    # Create unique username
    timestamp = int(time.time())
    test_username = f"test_user_{timestamp}"
    
    # Try to create user with minimal fields
    try:
        print("\nCREATING USER WITH MINIMAL FIELDS:")
        user1 = Users(
            username=test_username,
            extension=1001,
            group=group,
            groupname=group.enname.lower(),
            password=make_password("123456"),
            name="Test",
            lastname="User",
            picurl="avatar.png",
            active=True,
            needs_password_change=True
        )
        
        # Set fields explicitly to defaults if needed
        user1.email = ""
        user1.usersextension = []
        
        # Print what we're trying to save
        print(f"Username: {user1.username}")
        print(f"Extension: {user1.extension}")
        print(f"Group ID: {user1.group.id}")
        print(f"Group Name: {user1.groupname}")
        
        # Try to save
        print("\nSaving user...")
        user1.save()
        print(f"User saved successfully with ID: {user1.id}")
        
    except Exception as e:
        print(f"ERROR creating user: {e}")
        traceback.print_exc()
    
    # Check if user was created
    try:
        # Refresh from database
        user_count_after = Users.objects.count()
        print(f"\nUsers after: {user_count_after}")
        print(f"Difference: {user_count_after - user_count_before}")
        
        # Try to retrieve the user
        created_user = Users.objects.filter(username=test_username).first()
        if created_user:
            print(f"User found in database with ID: {created_user.id}")
        else:
            print("User NOT found in database!")
    except Exception as e:
        print(f"ERROR checking user: {e}")
        traceback.print_exc()
    
    # Try creating complete user with related objects
    try:
        print("\n" + "=" * 50)
        print("CREATING COMPLETE USER:")
        
        timestamp = int(time.time())
        complete_username = f"complete_user_{timestamp}"
        
        # Create user
        complete_user = Users(
            username=complete_username,
            extension=2001,
            group=group,
            groupname=group.enname.lower(),
            password=make_password("123456"),
            name="Complete",
            lastname="User",
            picurl="avatar.png",
            active=True,
            needs_password_change=True,
            usersextension=[]
        )
        
        print("Saving main user object...")
        complete_user.save()
        print(f"User saved with ID: {complete_user.id}")
        
        # Create permissions
        print("Creating permissions...")
        perm = Permissions(
            user=complete_user,
            can_view=True,
            can_write=False,
            can_delete=False,
            can_modify=False,
            exts_label=[]
        )
        perm.save()
        print(f"Permissions saved with ID: {perm.id}")
        
        # Create info
        print("Creating info record...")
        info = Infos(
            user=complete_user,
            gender=0,  # Male
            nationalcode=None,
            birthdate=None,
            telephone=None,
            phonenumber=None,
            maritalstatus='1',  # Single
            military='1',  # Completed
            educationfield=None,
            educationdegree='3',  # Bachelor
            province='7',  # Tehran
            city=None,
            address=None
        )
        info.save()
        print(f"Info saved with ID: {info.id}")
        
        print("\nComplete user creation successful!")
        
    except Exception as e:
        print(f"ERROR creating complete user: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_user_creation() 