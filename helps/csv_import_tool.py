#!/usr/bin/env python
"""
CSV Import Tool for Lotus Database
این ابزار برای وارد کردن فایل‌های CSV به جداول مختلف دیتابیس استفاده می‌شود
"""

import os
import sys
import csv
import django
import argparse
from datetime import datetime
from pathlib import Path

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')
django.setup()

from django.db import transaction
from django.contrib.auth.hashers import make_password
from Alvand.models import (
    Users, Groups, Infos, Permissions, Records, Faults, 
    Errors, Device, Telephons, Costs, Countries, 
    Extensionsgroups, Emailsending, Verifications, 
    PasswordResetRequest, Log, ContactInfo, errorsSent, 
    lices, SMDRRecord
)

class CSVImporter:
    def __init__(self, csv_file, model_class, update_existing=False, skip_errors=False):
        self.csv_file = csv_file
        self.model_class = model_class
        self.update_existing = update_existing
        self.skip_errors = skip_errors
        self.success_count = 0
        self.error_count = 0
        self.skipped_count = 0
        
    def detect_delimiter(self, file_path):
        """تشخیص جداکننده فایل CSV"""
        with open(file_path, 'r', encoding='utf-8') as file:
            sample = file.read(1024)
            file.seek(0)
            
            delimiters = [',', ';', '\t', '|']
            for delimiter in delimiters:
                if delimiter in sample:
                    return delimiter
            return ','
    
    def import_users(self):
        """وارد کردن کاربران از CSV"""
        print(f"🔄 شروع import کاربران از {self.csv_file}")
        
        delimiter = self.detect_delimiter(self.csv_file)
        print(f"📊 جداکننده تشخیص داده شده: '{delimiter}'")
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            print(f"📋 ستون‌های CSV: {list(reader.fieldnames)}")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    with transaction.atomic():
                        # بررسی فیلدهای اجباری
                        username = row.get('username', '').strip()
                        if not username:
                            if self.skip_errors:
                                print(f"⚠️  ردیف {row_num}: رد شد - نام کاربری خالی است")
                                self.skipped_count += 1
                                continue
                            else:
                                raise ValueError(f"ردیف {row_num}: نام کاربری اجباری است")
                        
                        # بررسی وجود کاربر
                        user_exists = Users.objects.filter(username=username).exists()
                        if user_exists and not self.update_existing:
                            if self.skip_errors:
                                print(f"⚠️  ردیف {row_num}: رد شد - کاربر {username} قبلاً وجود دارد")
                                self.skipped_count += 1
                                continue
                            else:
                                raise ValueError(f"ردیف {row_num}: کاربر {username} قبلاً وجود دارد")
                        
                        # ایجاد یا به‌روزرسانی کاربر
                        user_data = {
                            'username': username,
                            'name': row.get('name', ''),
                            'lastname': row.get('lastname', ''),
                            'email': row.get('email', ''),
                            'extension': row.get('extension', -1),
                            'active': self._parse_boolean(row.get('active', 'true')),
                            'online': int(row.get('online', 0)),
                            'picurl': row.get('picurl', ''),
                            'profile_picture': row.get('profile_picture', ''),
                            'needs_password_change': self._parse_boolean(row.get('needs_password_change', 'false'))
                        }
                        
                        # ایجاد گروه پیش‌فرض اگر وجود نداشته باشد
                        default_group, created = Groups.objects.get_or_create(
                            pename='کاربران پیش‌فرض',
                            enname='Default Users',
                            defaults={'active': True}
                        )
                        user_data['group'] = default_group
                        
                        # رمزگذاری رمز عبور
                        if row.get('password'):
                            user_data['password'] = make_password(row['password'])
                        
                        if user_exists and self.update_existing:
                            Users.objects.filter(username=username).update(**user_data)
                            user = Users.objects.get(username=username)
                            print(f"✅ ردیف {row_num}: کاربر {username} به‌روزرسانی شد")
                        else:
                            user = Users.objects.create(**user_data)
                            print(f"✅ ردیف {row_num}: کاربر {username} ایجاد شد")
                        
                        # ایجاد اطلاعات اضافی
                        self._create_user_info(user, row, row_num)
                        
                        # ایجاد مجوزها
                        self._create_user_permissions(user, row, row_num)
                        
                        self.success_count += 1
                        
                except Exception as e:
                    self.error_count += 1
                    print(f"❌ ردیف {row_num}: خطا - {str(e)}")
                    if not self.skip_errors:
                        raise
    
    def _parse_boolean(self, value):
        """تبدیل مقادیر مختلف به boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'y', 'on']
        return bool(value)
    
    def _create_user_info(self, user, row, row_num):
        """ایجاد اطلاعات اضافی کاربر"""
        info_data = {
            'user': user,
            'phonenumber': row.get('phonenumber', ''),
            'telephone': row.get('telephone', ''),
            'province': row.get('province', ''),
            'city': row.get('city', ''),
            'address': row.get('address', ''),
            'gender': row.get('gender', '2'),
            'military': row.get('military', ''),
            'maritalstatus': row.get('maritalstatus', ''),
            'educationdegree': row.get('educationdegree', ''),
            'educationfield': row.get('educationfield', ''),
            'cardnumber': row.get('cardnumber', ''),
            'accountnumber': row.get('accountnumber', ''),
            'accountnumbershaba': row.get('accountnumbershaba', ''),
            'macaddress': row.get('macaddress', ''),
            'nationalcode': row.get('nationalcode', '')
        }
        
        # حذف فیلدهای خالی
        info_data = {k: v for k, v in info_data.items() if v}
        
        if info_data:
            Infos.objects.update_or_create(
                user=user,
                defaults=info_data
            )
    
    def _create_user_permissions(self, user, row, row_num):
        """ایجاد مجوزهای کاربر"""
        perm_data = {
            'user': user,
            'perm_email': self._parse_boolean(row.get('perm_email', 'false')),
            'can_view': self._parse_boolean(row.get('can_view', 'false')),
            'can_write': self._parse_boolean(row.get('can_write', 'false')),
            'can_delete': self._parse_boolean(row.get('can_delete', 'false')),
            'can_modify': self._parse_boolean(row.get('can_modify', 'false')),
            'errorsreport': self._parse_boolean(row.get('errorsreport', 'false'))
        }
        
        # پردازش فیلدهای آرایه‌ای
        if row.get('exts_label'):
            perm_data['exts_label'] = [x.strip() for x in row['exts_label'].split(',')]
        if row.get('usersextension'):
            perm_data['usersextension'] = [x.strip() for x in row['usersextension'].split(',')]
        
        Permissions.objects.update_or_create(
            user=user,
            defaults=perm_data
        )
    
    def import_records(self):
        """وارد کردن رکوردها از CSV"""
        print(f"🔄 شروع import رکوردها از {self.csv_file}")
        
        delimiter = self.detect_delimiter(self.csv_file)
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            print(f"📋 ستون‌های CSV: {list(reader.fieldnames)}")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    with transaction.atomic():
                        record_data = {
                            'extension': row.get('extension', ''),
                            'caller': row.get('caller', ''),
                            'called': row.get('called', ''),
                            'duration': int(row.get('duration', 0)),
                            'call_type': row.get('call_type', ''),
                            'date': self._parse_date(row.get('date')),
                            'time': row.get('time', ''),
                            'cost': float(row.get('cost', 0.0))
                        }
                        
                        Records.objects.create(**record_data)
                        print(f"✅ ردیف {row_num}: رکورد ایجاد شد")
                        self.success_count += 1
                        
                except Exception as e:
                    self.error_count += 1
                    print(f"❌ ردیف {row_num}: خطا - {str(e)}")
                    if not self.skip_errors:
                        raise
    
    def _parse_date(self, date_str):
        """تبدیل رشته تاریخ به datetime"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return None
    
    def import_smdr_records(self):
        """وارد کردن رکوردهای SMDR از CSV"""
        print(f"🔄 شروع import رکوردهای SMDR از {self.csv_file}")
        
        delimiter = self.detect_delimiter(self.csv_file)
        
        with open(self.csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            print(f"📋 ستون‌های CSV: {list(reader.fieldnames)}")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    with transaction.atomic():
                        smdr_data = {
                            'extension': row.get('extension', ''),
                            'caller_number': row.get('caller_number', ''),
                            'called_number': row.get('called_number', ''),
                            'duration': int(row.get('duration', 0)),
                            'call_type': row.get('call_type', ''),
                            'date_time': self._parse_datetime(row.get('date_time')),
                            'cost': float(row.get('cost', 0.0)),
                            'account_code': row.get('account_code', '')
                        }
                        
                        SMDRRecord.objects.create(**smdr_data)
                        print(f"✅ ردیف {row_num}: رکورد SMDR ایجاد شد")
                        self.success_count += 1
                        
                except Exception as e:
                    self.error_count += 1
                    print(f"❌ ردیف {row_num}: خطا - {str(e)}")
                    if not self.skip_errors:
                        raise
    
    def _parse_datetime(self, datetime_str):
        """تبدیل رشته datetime به datetime object"""
        if not datetime_str:
            return None
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except:
            return None
    
    def print_summary(self):
        """نمایش خلاصه نتایج"""
        print(f"\n📊 خلاصه نتایج:")
        print(f"✅ موفق: {self.success_count}")
        print(f"❌ خطا: {self.error_count}")
        print(f"⚠️  رد شده: {self.skipped_count}")
        print(f"📈 کل: {self.success_count + self.error_count + self.skipped_count}")

def main():
    parser = argparse.ArgumentParser(description='ابزار وارد کردن فایل‌های CSV به دیتابیس')
    parser.add_argument('csv_file', help='مسیر فایل CSV')
    parser.add_argument('--model', choices=['users', 'records', 'smdr'], 
                       default='users', help='نوع مدل برای import')
    parser.add_argument('--update', action='store_true', 
                       help='به‌روزرسانی رکوردهای موجود به جای ایجاد جدید')
    parser.add_argument('--skip-errors', action='store_true', 
                       help='رد کردن خطاها و ادامه پردازش')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.csv_file):
        print(f"❌ فایل CSV یافت نشد: {args.csv_file}")
        return
    
    # ایجاد نمونه importer
    importer = CSVImporter(
        csv_file=args.csv_file,
        model_class=args.model,
        update_existing=args.update,
        skip_errors=args.skip_errors
    )
    
    try:
        # اجرای import بر اساس نوع مدل
        if args.model == 'users':
            importer.import_users()
        elif args.model == 'records':
            importer.import_records()
        elif args.model == 'smdr':
            importer.import_smdr_records()
        
        importer.print_summary()
        
    except KeyboardInterrupt:
        print("\n⏹️  عملیات توسط کاربر متوقف شد")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
