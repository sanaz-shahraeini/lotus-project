import os
import django
import sys
import traceback

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from django.test.client import Client
from Alvand.models import Users, Groups, Permissions, Infos

def debug_form_submission():
    print("=" * 50)
    print("FORM SUBMISSION DEBUGGING")
    print("=" * 50)
    
    # Create a test user directly
    try:
        # Check for existing test user
        username = 'test_user_direct'
        test_user = Users.objects.filter(username=username).first()
        
        if test_user:
            print(f"Using existing test user: {test_user.username}")
        else:
            # Get a group for the user
            group = Groups.objects.filter(enname__iexact='member').first()
            if not group:
                group = Groups.objects.first()
                
            if not group:
                print("No group found in database!")
                return
                
            print(f"Creating test user with group: {group.enname}")
            
            # Create user directly with the ORM
            test_user = Users.objects.create(
                username=username,
                name="Test",
                lastname="User Direct",
                extension=1001,
                email="test@example.com",
                group=group,
                groupname=group.enname.lower(),
                active=True,
                usersextension=[],
                password=make_password("123456"),
                picurl="avatar.png",
                needs_password_change=True
            )
            
            # Create permissions
            Permissions.objects.create(
                user=test_user,
                can_view=True,
                can_write=True,
                can_modify=True,
                can_delete=True,
                exts_label=[]
            )
            
            # Create user info
            Infos.objects.create(
                user=test_user,
                gender=0,
                nationalcode=None,
                birthdate=None,
                telephone=None,
                phonenumber=None,
                maritalstatus='1',
                military='1',
                educationfield=None,
                educationdegree='3',
                province='7',
                city=None,
                address=None
            )
            
            print(f"Created test user with ID: {test_user.id}")
        
        # Test direct form submission without using Client
        print("\nTesting direct user creation...")
        
        # Get a supporter group for new user
        supporter_group = Groups.objects.filter(enname__iexact='supporter').first()
        if not supporter_group:
            supporter_group = Groups.objects.first()
            print(f"No supporter group found, using group: {supporter_group.enname}")
        
        # Generate unique username
        import time
        test_username = f"direct_test_{int(time.time())}"
        
        print(f"Creating user with username: {test_username}")
        
        # Create user directly
        new_user = Users.objects.create(
            username=test_username,
            name="Direct",
            lastname="Test",
            extension=2001,
            email="direct@test.com",
            group=supporter_group,
            groupname=supporter_group.enname.lower(),
            picurl="avatar.png",
            active=True,
            usersextension=[],
            password=make_password("123456789"),
            needs_password_change=True
        )
        
        print(f"User created with ID: {new_user.id}")
        
        # Create permissions
        perm = Permissions.objects.create(
            user=new_user,
            can_view=True,
            can_write=False,
            can_delete=False,
            can_modify=False,
            exts_label=[]
        )
        print(f"Permissions created with ID: {perm.id}")
        
        # Create user info
        info = Infos.objects.create(
            user=new_user,
            gender=0,
            nationalcode=None,
            birthdate=None,
            telephone=None,
            phonenumber=None,
            maritalstatus='1',
            military='1',
            educationfield=None,
            educationdegree='3',
            province='7',
            city=None,
            address=None
        )
        print(f"User info created with ID: {info.id}")
        
        print("\nVerifying user creation...")
        db_user = Users.objects.get(id=new_user.id)
        print(f"Username: {db_user.username}")
        print(f"Name: {db_user.name} {db_user.lastname}")
        print(f"Extension: {db_user.extension}")
        print(f"Group: {db_user.groupname}")
        print("User created successfully!")
        
        print("\nCleaning up - deleting test user...")
        new_user.delete()
        print("Test user deleted")
        
    except Exception as e:
        print(f"Error during debug: {str(e)}")
        traceback.print_exc()
    
if __name__ == "__main__":
    debug_form_submission() 