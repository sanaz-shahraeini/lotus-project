# CSV Import for Users

This Django management command allows you to import users from CSV files into your database.

## Features

- **Automatic delimiter detection** (comma, semicolon, tab, pipe)
- **UTF-8 encoding support** for Persian text
- **Transaction safety** - all operations are atomic
- **Flexible field mapping** with sensible defaults
- **Error handling** with options to skip problematic rows
- **Update existing users** or create new ones
- **Automatic group creation** if needed
- **Related model support** (Infos, Permissions)

## CSV Format

Your CSV file should have the following columns (all are optional except `username`):

### Required Fields
- `username` - Unique username (required)

### User Fields
- `name` - First name
- `lastname` - Last name
- `email` - Email address
- `extension` - Extension number
- `active` - Active status (true/false, 1/0, yes/no)
- `online` - Online status (1/0)
- `picurl` - Profile picture URL
- `profile_picture` - Profile picture path
- `password` - Password (will be hashed automatically)
- `needs_password_change` - Force password change (true/false)

### Info Fields
- `phonenumber` - Mobile phone number
- `telephone` - Landline phone number
- `province` - Province (use numeric codes: 7=تهران, etc.)
- `city` - City name
- `address` - Full address
- `gender` - Gender (0=مرد, 1=زن, 2=نامعلوم)
- `military` - Military status (0=مشمول, 1=پایان خدمت, 2=معافیت پزشکی, 3=معافیت تحصیلی, 4=معافیت سایر)
- `maritalstatus` - Marital status (0=متاهل, 1=مجرد)
- `educationdegree` - Education degree (0=زیر دیپلم, 1=دیپلم, 2=فوق دیپلم, 3=لیسانس, 4=فوق لیسانس, 5=دکترا, 6=فوق دکترا)
- `educationfield` - Field of study
- `cardnumber` - Card number
- `accountnumber` - Account number
- `accountnumbershaba` - Shaba account number
- `macaddress` - MAC address
- `nationalcode` - National ID number
- `groupname` - Group name

### Permission Fields
- `perm_email` - Email permission (true/false)
- `can_view` - View permission (true/false)
- `can_write` - Write permission (true/false)
- `can_delete` - Delete permission (true/false)
- `can_modify` - Modify permission (true/false)
- `errorsreport` - Error report permission (true/false)
- `exts_label` - Extension labels (comma-separated)
- `usersextension` - User extensions (comma-separated)

## Usage

### Basic Import
```bash
python manage.py import_users_csv path/to/your/file.csv
```

### Update Existing Users
```bash
python manage.py import_users_csv path/to/your/file.csv --update
```

### Skip Errors and Continue
```bash
python manage.py import_users_csv path/to/your/file.csv --skip-errors
```

### Combine Options
```bash
python manage.py import_users_csv path/to/your/file.csv --update --skip-errors
```

## Examples

### Example 1: Basic Import
```bash
python manage.py import_users_csv users.csv
```

### Example 2: Update Existing Users
```bash
python manage.py import_users_csv updated_users.csv --update
```

### Example 3: Import with Error Handling
```bash
python manage.py import_users_csv users.csv --skip-errors
```

## CSV Examples

### Simple User
```csv
username,name,lastname,email,extension
john,جان,دو,john@example.com,101
```

### Full User with All Fields
```csv
username,name,lastname,email,extension,active,online,phonenumber,province,gender,can_view,can_write
admin,مدیر,سیستم,admin@example.com,100,true,1,09123456789,7,0,true,true
```

## Field Mapping

### Boolean Fields
These fields accept various formats:
- `true`, `1`, `yes`, `y`, `on` → True
- `false`, `0`, `no`, `n`, `off` → False

### Choice Fields
Use the numeric codes as defined in your models:
- **Gender**: 0=مرد, 1=زن, 2=نامعلوم
- **Province**: 7=تهران, 4=البرز, etc.
- **Military**: 0=مشمول, 1=پایان خدمت, etc.

### Array Fields
For fields like `exts_label` and `usersextension`, use comma-separated values:
```csv
username,exts_label,usersextension
admin,"100,101,102","100,101,102"
```

## Error Handling

The command provides detailed error reporting:
- **Row numbers** for easy identification
- **Specific error messages** for debugging
- **Option to skip errors** and continue processing
- **Summary report** at the end

## Tips

1. **Test with a small file first** to ensure your format is correct
2. **Use UTF-8 encoding** for Persian text
3. **Check field names** match exactly (case-sensitive)
4. **Use the sample template** as a starting point
5. **Backup your database** before large imports

## Troubleshooting

### Common Issues

1. **"No username provided"** - Ensure username column exists and has values
2. **"User already exists"** - Use `--update` flag or remove duplicate usernames
3. **"Invalid choice"** - Check choice field values match the expected codes
4. **"CSV file not found"** - Verify the file path is correct

### Getting Help

Run the command with `--help` for detailed options:
```bash
python manage.py import_users_csv --help
```

