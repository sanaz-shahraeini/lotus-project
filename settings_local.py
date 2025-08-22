# Local PostgreSQL Database Configuration
# Copy this to replace the DATABASES section in lotus/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lotusdb',
        'USER': 'postgres',  # or 'lotusdb_owner' if you created a specific user
        'PASSWORD': 'your_local_password',  # UPDATE THIS with your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
        # Remove SSL requirement for local database
        # 'OPTIONS': {
        #     'sslmode': 'require',
        # },
    }
}

# Alternative configuration using environment variables (recommended)
# Create a .env file with:
# DB_PASSWORD=your_actual_password

# import os
# from dotenv import load_dotenv
# load_dotenv()

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'lotusdb',
#         'USER': 'postgres',
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
