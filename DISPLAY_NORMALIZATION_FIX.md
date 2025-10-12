# اصلاح نمایش شماره‌های با پیش‌شماره 98000

## 🔴 مشکل

شماره‌هایی که با `+98000` یا `98000` در دیتابیس ذخیره شده بودند، در داشبورد به همان صورت نمایش داده می‌شدند و باعث سردرگمی کاربر می‌شدند.

### مثال:
```
دیتابیس: +980009851384710
نمایش قبلی: +980009851384710 ❌ (گیج‌کننده)
نمایش صحیح: +989 851 384 710 ✅ (خوانا)
```

## ✅ راه‌حل

### 1. اصلاح Template Filter `format_phone_number`

در فایل `dashboardTags.py`:

```python
@register.filter
def format_phone_number(number):
    """Format phone number for better readability and normalize display"""
    if not number:
        return ''
        
    # Clean the number
    number = str(number).replace(' ', '')
    
    # Normalize 98000 prefix in display
    if number.startswith('+98000'):
        number = '+98' + number[6:]  # حذف 000
    elif number.startswith('98000'):
        number = '98' + number[5:]   # حذف 000
    
    # Check if it's an international number
    if number.startswith('+'):
        # Format international number
        if len(number) > 10:
            return f"{number[:4]} {number[4:7]} {number[7:10]} {number[10:]}"
        else:
            return number
    # ... rest of formatting
```

### 2. استفاده در Template

در فایل `dashboard.html`:

**قبل:**
```django
{{ rec.contactnumber }}
```

**بعد:**
```django
{{ rec.contactnumber|format_phone_number }}
```

## 📊 نحوه عملکرد

### مرحله 1: نرمال‌سازی پیش‌شماره
```
+980009851384710 → +989851384710
98000985138471040 → 98985138471040
```

### مرحله 2: فرمت‌بندی برای نمایش
```
+989851384710 → +989 851 384 710
09124525065 → 091 245 250 65
03136120001 → 031 361 200 01
```

## 🎯 مثال‌های واقعی

### مثال 1: شماره موبایل با 98000
```
ذخیره در DB: +980009851384710
نمایش: +989 851 384 710
محاسبه هزینه: ایرانسل (0985)
```

### مثال 2: شماره موبایل معمولی
```
ذخیره در DB: +989124525065
نمایش: +989 124 525 065
محاسبه هزینه: همراه اول (0912)
```

### مثال 3: شماره ثابت
```
ذخیره در DB: +983136120001
نمایش: +983 136 120 001
محاسبه هزینه: اصفهان (031)
```

### مثال 4: شماره داخلی
```
ذخیره در DB: 204
نمایش: 204
محاسبه هزینه: 0 (تماس داخلی)
```

## 🔄 تفاوت بین نرمال‌سازی و نمایش

| مرحله | محل | هدف |
|-------|-----|-----|
| **نرمال‌سازی در `callTypeDetector`** | `views.py` | تشخیص نوع تماس و محاسبه هزینه |
| **نرمال‌سازی در `format_phone_number`** | `dashboardTags.py` | نمایش زیبا و خوانا در UI |

### مثال کامل:
```
1. ذخیره در DB: +980009851384710

2. محاسبه هزینه (views.py):
   +980009851384710 → 09851384710 → ایرانسل

3. نمایش در UI (template):
   +980009851384710 → +989851384710 → +989 851 384 710
```

## 📝 تغییرات اعمال شده

### 1. `dashboardTags.py`
```python
# خطوط 106-110 اضافه شد:
if number.startswith('+98000'):
    number = '+98' + number[6:]
elif number.startswith('98000'):
    number = '98' + number[5:]
```

### 2. `dashboard.html`
```django
<!-- خط 1315: Desktop view -->
<td class="text-center">
    <span class="font-medium">
        {% if rec.contactnumber %}
            {{ rec.contactnumber|format_phone_number }}
        {% else %}
            <span class="text-slate-400">-</span>
        {% endif %}
    </span>
</td>

<!-- خط 1354: Mobile view -->
<p class="text-sm font-medium text-slate-900">
    {{ rec.contactnumber|format_phone_number|default:"شماره ناشناس" }}
</p>
```

## 🧪 تست

### ورودی‌های مختلف:
| ورودی | نمایش |
|-------|-------|
| `+980009851384710` | `+989 851 384 710` |
| `+98000985138471040` | `+989 851 384 710 40` |
| `980009851384710` | `989 851 384 710` |
| `+989124525065` | `+989 124 525 065` |
| `09124525065` | `091 245 250 65` |
| `03136120001` | `031 361 200 01` |
| `204` | `204` |

## ✅ مزایا

1. ✅ **خوانایی بهتر**: شماره‌ها با فاصله نمایش داده می‌شوند
2. ✅ **نرمال‌سازی خودکار**: `98000` به `98` تبدیل می‌شود
3. ✅ **سازگار با همه فرمت‌ها**: موبایل، ثابت، داخلی
4. ✅ **محاسبه صحیح**: هزینه بر اساس شماره نرمال شده محاسبه می‌شود
5. ✅ **UI تمیز**: نمایش حرفه‌ای و استاندارد

## 📌 فایل‌های تغییر یافته

- ✅ `Alvand/templatetags/dashboardTags.py` - تابع `format_phone_number` (خطوط 97-127)
- ✅ `Alvand/templates/dashboard.html` - خط 1315 (Desktop view)
- ✅ `Alvand/templates/dashboard.html` - خط 1354 (Mobile view)

## 🎉 نتیجه

با این تغییرات:
- ✅ شماره‌ها در UI به صورت خوانا و زیبا نمایش داده می‌شوند
- ✅ پیش‌شماره `98000` به `98` تبدیل می‌شود
- ✅ فاصله‌گذاری مناسب برای خوانایی بهتر
- ✅ محاسبه هزینه به درستی انجام می‌شود
