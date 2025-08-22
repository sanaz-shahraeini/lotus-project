# راهنمای سریع وارد کردن CSV

## 🚀 شروع سریع

### روش 1: استفاده از فایل Batch (ساده‌ترین روش)
```bash
# دوبار کلیک روی فایل
import_csv.bat
```

### روش 2: استفاده از خط فرمان
```bash
# فعال کردن محیط مجازی
venv\Scripts\activate

# وارد کردن کاربران
python csv_import_tool.py sample_users.csv --model users

# وارد کردن رکوردها
python csv_import_tool.py sample_records.csv --model records

# وارد کردن رکوردهای SMDR
python csv_import_tool.py sample_smdr.csv --model smdr
```

### روش 3: استفاده از Django Commands
```bash
# وارد کردن کاربران
python manage.py import_users_csv sample_users.csv

# وارد کردن رکوردها
python manage.py import_records sample_records.csv

# وارد کردن رکوردهای SMDR
python manage.py import_smdr sample_smdr.csv
```

## 📁 فایل‌های نمونه

- `sample_users.csv` - نمونه کاربران
- `sample_records.csv` - نمونه رکوردها
- `sample_smdr.csv` - نمونه رکوردهای SMDR

## ⚙️ گزینه‌های پیشرفته

### به‌روزرسانی رکوردهای موجود
```bash
python csv_import_tool.py users.csv --model users --update
```

### رد کردن خطاها و ادامه
```bash
python csv_import_tool.py users.csv --model users --skip-errors
```

### ترکیب گزینه‌ها
```bash
python csv_import_tool.py users.csv --model users --update --skip-errors
```

## 📋 فرمت فایل CSV

### کاربران (ستون‌های اجباری)
```csv
username,name,lastname,email,extension
admin,مدیر,سیستم,admin@example.com,100
```

### رکوردها
```csv
extension,caller,called,duration,call_type,date,time,cost
100,09123456789,02112345678,120,outgoing,2024-01-15,14:30:00,50.0
```

### رکوردهای SMDR
```csv
extension,caller_number,called_number,duration,call_type,date_time,cost,account_code
100,09123456789,02112345678,120,outgoing,2024-01-15 14:30:00,50.0,ACC001
```

## ⚠️ نکات مهم

1. **Encoding**: از UTF-8 استفاده کنید
2. **Backup**: قبل از import بزرگ، از دیتابیس backup بگیرید
3. **Test**: ابتدا با فایل کوچک تست کنید
4. **Headers**: ستون اول باید header باشد

## 🆘 عیب‌یابی

### خطای "فایل یافت نشد"
- مسیر فایل را بررسی کنید
- از مسیر کامل استفاده کنید

### خطای "نام کاربری اجباری است"
- ستون `username` را بررسی کنید
- فیلدهای خالی را پر کنید

### خطای "کاربر قبلاً وجود دارد"
- از `--update` استفاده کنید
- یا `--skip-errors` اضافه کنید

## 📞 پشتیبانی

برای اطلاعات بیشتر، فایل `CSV_IMPORT_GUIDE.md` را مطالعه کنید.
