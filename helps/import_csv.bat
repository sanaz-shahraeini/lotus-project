@echo off
chcp 65001 >nul
echo ========================================
echo ابزار وارد کردن فایل‌های CSV به دیتابیس
echo ========================================
echo.

REM فعال کردن محیط مجازی
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ محیط مجازی فعال شد
) else (
    echo ❌ محیط مجازی یافت نشد
    pause
    exit /b 1
)

echo.
echo انتخاب نوع import:
echo 1. وارد کردن کاربران
echo 2. وارد کردن رکوردها
echo 3. وارد کردن رکوردهای SMDR
echo 4. خروج
echo.

set /p choice="لطفاً گزینه مورد نظر را انتخاب کنید (1-4): "

if "%choice%"=="1" goto import_users
if "%choice%"=="2" goto import_records
if "%choice%"=="3" goto import_smdr
if "%choice%"=="4" goto exit
goto invalid_choice

:import_users
echo.
echo ========================================
echo وارد کردن کاربران
echo ========================================
echo.
set /p csv_file="مسیر فایل CSV کاربران: "
if not exist "%csv_file%" (
    echo ❌ فایل یافت نشد: %csv_file%
    pause
    exit /b 1
)

echo.
echo گزینه‌های اضافی:
echo 1. ایجاد کاربران جدید (پیش‌فرض)
echo 2. به‌روزرسانی کاربران موجود
echo 3. رد کردن خطاها و ادامه
echo 4. هر دو گزینه بالا
echo.

set /p update_choice="انتخاب کنید (1-4): "

if "%update_choice%"=="1" (
    python csv_import_tool.py "%csv_file%" --model users
) else if "%update_choice%"=="2" (
    python csv_import_tool.py "%csv_file%" --model users --update
) else if "%update_choice%"=="3" (
    python csv_import_tool.py "%csv_file%" --model users --skip-errors
) else if "%update_choice%"=="4" (
    python csv_import_tool.py "%csv_file%" --model users --update --skip-errors
) else (
    python csv_import_tool.py "%csv_file%" --model users
)
goto end

:import_records
echo.
echo ========================================
echo وارد کردن رکوردها
echo ========================================
echo.
set /p csv_file="مسیر فایل CSV رکوردها: "
if not exist "%csv_file%" (
    echo ❌ فایل یافت نشد: %csv_file%
    pause
    exit /b 1
)

python csv_import_tool.py "%csv_file%" --model records --skip-errors
goto end

:import_smdr
echo.
echo ========================================
echo وارد کردن رکوردهای SMDR
echo ========================================
echo.
set /p csv_file="مسیر فایل CSV رکوردهای SMDR: "
if not exist "%csv_file%" (
    echo ❌ فایل یافت نشد: %csv_file%
    pause
    exit /b 1
)

python csv_import_tool.py "%csv_file%" --model smdr --skip-errors
goto end

:invalid_choice
echo ❌ انتخاب نامعتبر
pause
exit /b 1

:end
echo.
echo ========================================
echo عملیات تکمیل شد
echo ========================================
pause

:exit
echo خروج...

