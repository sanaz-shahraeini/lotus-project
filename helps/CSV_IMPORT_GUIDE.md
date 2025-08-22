# راهنمای وارد کردن فایل‌های CSV به دیتابیس

این راهنما به شما کمک می‌کند تا فایل‌های CSV را به جداول مختلف دیتابیس لوکال خود وارد کنید.

## ابزارهای موجود

### 1. ابزار جامع CSV Import (`csv_import_tool.py`)
ابزار جدید و پیشرفته برای وارد کردن انواع مختلف داده‌ها

### 2. Django Management Commands
- `import_users_csv` - وارد کردن کاربران
- `import_records` - وارد کردن رکوردها
- `import_smdr` - وارد کردن رکوردهای SMDR

## استفاده از ابزار جامع

### نصب و راه‌اندازی
```bash
# اطمینان از فعال بودن محیط مجازی
venv\Scripts\activate

# اجرای ابزار
python csv_import_tool.py [فایل_CSV] --model [نوع_مدل]
```

### پارامترهای ابزار

#### پارامترهای اجباری:
- `csv_file`: مسیر فایل CSV

#### پارامترهای اختیاری:
- `--model`: نوع مدل (users, records, smdr) - پیش‌فرض: users
- `--update`: به‌روزرسانی رکوردهای موجود به جای ایجاد جدید
- `--skip-errors`: رد کردن خطاها و ادامه پردازش

### مثال‌های استفاده

#### 1. وارد کردن کاربران
```bash
# وارد کردن کاربران جدید
python csv_import_tool.py users.csv --model users

# به‌روزرسانی کاربران موجود
python csv_import_tool.py users.csv --model users --update

# وارد کردن با رد کردن خطاها
python csv_import_tool.py users.csv --model users --skip-errors
```

#### 2. وارد کردن رکوردها
```bash
python csv_import_tool.py records.csv --model records
```

#### 3. وارد کردن رکوردهای SMDR
```bash
python csv_import_tool.py smdr_records.csv --model smdr
```

## فرمت فایل‌های CSV

### 1. فایل CSV کاربران

#### ستون‌های اجباری:
- `username`: نام کاربری (منحصر به فرد)

#### ستون‌های اختیاری کاربر:
- `name`: نام
- `lastname`: نام خانوادگی
- `email`: ایمیل
- `extension`: شماره داخلی
- `active`: وضعیت فعال (true/false, 1/0, yes/no)
- `online`: وضعیت آنلاین (1/0)
- `picurl`: آدرس تصویر پروفایل
- `profile_picture`: مسیر تصویر پروفایل
- `password`: رمز عبور (خودکار رمزگذاری می‌شود)
- `needs_password_change`: نیاز به تغییر رمز (true/false)

#### ستون‌های اطلاعات اضافی:
- `phonenumber`: شماره موبایل
- `telephone`: شماره تلفن ثابت
- `province`: استان (کد عددی: 7=تهران، 4=البرز، ...)
- `city`: شهر
- `address`: آدرس کامل
- `gender`: جنسیت (0=مرد، 1=زن، 2=نامعلوم)
- `military`: وضعیت نظام وظیفه (0=مشمول، 1=پایان خدمت، ...)
- `maritalstatus`: وضعیت تاهل (0=متاهل، 1=مجرد)
- `educationdegree`: مدرک تحصیلی (0=زیر دیپلم، 1=دیپلم، ...)
- `educationfield`: رشته تحصیلی
- `cardnumber`: شماره کارت
- `accountnumber`: شماره حساب
- `accountnumbershaba`: شماره شبا
- `macaddress`: آدرس MAC
- `nationalcode`: کد ملی

#### ستون‌های مجوزها:
- `perm_email`: مجوز ایمیل (true/false)
- `can_view`: مجوز مشاهده (true/false)
- `can_write`: مجوز نوشتن (true/false)
- `can_delete`: مجوز حذف (true/false)
- `can_modify`: مجوز ویرایش (true/false)
- `errorsreport`: مجوز گزارش خطا (true/false)
- `exts_label`: برچسب‌های داخلی (جدا شده با کاما)
- `usersextension`: داخلی‌های کاربر (جدا شده با کاما)

### 2. فایل CSV رکوردها

#### ستون‌های مورد نیاز:
- `extension`: شماره داخلی
- `caller`: شماره تماس گیرنده
- `called`: شماره تماس شونده
- `duration`: مدت تماس (ثانیه)
- `call_type`: نوع تماس
- `date`: تاریخ (YYYY-MM-DD)
- `time`: زمان
- `cost`: هزینه

### 3. فایل CSV رکوردهای SMDR

#### ستون‌های مورد نیاز:
- `extension`: شماره داخلی
- `caller_number`: شماره تماس گیرنده
- `called_number`: شماره تماس شونده
- `duration`: مدت تماس (ثانیه)
- `call_type`: نوع تماس
- `date_time`: تاریخ و زمان (YYYY-MM-DD HH:MM:SS)
- `cost`: هزینه
- `account_code`: کد حساب

## مثال‌های فایل CSV

### مثال 1: کاربر ساده
```csv
username,name,lastname,email,extension
john,جان,دو,john@example.com,101
```

### مثال 2: کاربر کامل
```csv
username,name,lastname,email,extension,active,online,phonenumber,province,gender,can_view,can_write
admin,مدیر,سیستم,admin@example.com,100,true,1,09123456789,7,0,true,true
```

### مثال 3: رکورد تماس
```csv
extension,caller,called,duration,call_type,date,time,cost
101,09123456789,02112345678,120,outgoing,2024-01-15,14:30:00,50.0
```

### مثال 4: رکورد SMDR
```csv
extension,caller_number,called_number,duration,call_type,date_time,cost,account_code
101,09123456789,02112345678,120,outgoing,2024-01-15 14:30:00,50.0,ACC001
```

## استفاده از Django Management Commands

### وارد کردن کاربران
```bash
python manage.py import_users_csv users.csv
python manage.py import_users_csv users.csv --update
python manage.py import_users_csv users.csv --skip-errors
```

### وارد کردن رکوردها
```bash
python manage.py import_records records.csv
```

### وارد کردن رکوردهای SMDR
```bash
python manage.py import_smdr smdr_records.csv
```

## نکات مهم

### 1. آماده‌سازی فایل CSV
- از **UTF-8 encoding** استفاده کنید
- ستون‌ها را با کاما (,) جدا کنید
- از فرمت تاریخ صحیح استفاده کنید
- فیلدهای خالی را خالی بگذارید

### 2. امنیت
- قبل از import بزرگ، از دیتابیس backup بگیرید
- ابتدا با فایل کوچک تست کنید
- رمزهای عبور در فایل CSV ذخیره نکنید

### 3. عملکرد
- برای فایل‌های بزرگ، از `--skip-errors` استفاده کنید
- import را در ساعات کم‌ترافیک انجام دهید
- از transaction استفاده کنید (خودکار انجام می‌شود)

### 4. عیب‌یابی
- خطاها را بررسی کنید
- فرمت فایل CSV را چک کنید
- ستون‌ها را با مدل تطبیق دهید

## کدهای استان‌ها

| کد | استان |
|----|-------|
| 0 | آذربایجان شرقی |
| 1 | آذربایجان غربی |
| 2 | اردبیل |
| 3 | اصفهان |
| 4 | البرز |
| 5 | ایلام |
| 6 | بوشهر |
| 7 | تهران |
| 8 | چهارمحال و بختیاری |
| 9 | خراسان جنوبی |
| 10 | خراسان رضوی |
| 11 | خراسان شمالی |
| 12 | خوزستان |
| 13 | زنجان |
| 14 | سمنان |
| 15 | سیستان و بلوچستان |
| 16 | فارس |
| 17 | قزوین |
| 18 | قم |
| 19 | کردستان |
| 20 | کرمان |
| 21 | کرمانشاه |
| 22 | کهگیلویه و بویراحمد |
| 23 | گلستان |
| 24 | گیلان |
| 25 | لرستان |
| 26 | مازندران |
| 27 | مرکزی |
| 28 | هرمزگان |
| 29 | همدان |
| 30 | یزد |

## پشتیبانی

در صورت بروز مشکل:
1. خطاها را بررسی کنید
2. فرمت فایل CSV را چک کنید
3. از فایل نمونه استفاده کنید
4. با تیم پشتیبانی تماس بگیرید
