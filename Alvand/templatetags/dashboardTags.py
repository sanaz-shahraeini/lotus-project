from django.template import Library
from Alvand.models import Records
import jdatetime, datetime
from Alvand.views import callTypeDetector, getPrice, calculatePrice

register = Library()

@register.filter
def convertDatesToHijri(date):
    try:
        y, m, d = map(int, date.replace("-", "/").split("/"))
        return jdatetime.datetime.fromgregorian(year=y, month=m, day=d).strftime("%Y/%m/%d")
    except:
        return date
    
@register.filter
def getRealCallType(callType):
    match callType.lower():
        case "incomingna":
            return "بدون پاسخ"  # 4007
        case "incomingrc":
            return "تماس دریافت شده"  # 4008
        case "incomingan":
            return "پاسخ داده شده"  # 4009
        case "transfer":
            return "انتقال داده شده"  # 4010
        case "incomingdisa":
            return "منشی خودکار"  # 4011
        case "incominghangup":
            return "پایان یافته"  # 4012
        case "extension":
            return "تماس داخلی"  # 4013
        case "outgoing":
            return "تماس خارجی"  # 4014
        case _:
            return "تماس ناشناخته"  # 4015
        
@register.filter
def getCallTypeIcon(callType):
    match getRealCallType(callType):
        case "تماس داخلی":
            return "IN.jpg"
        case "تماس خارجی":
            return "out.jpg"
        case "بدون پاسخ":
            return "NA.jpg"
        case _:
            return "AN.jpg"
        
@register.filter
def calculateOnePrice(duration, contactnumber):
    if not duration or not contactnumber:
        return '0'
    calltype = callTypeDetector(contactnumber)
    if calltype is None: return '0'
    price = getPrice(calltype)
    if price is None: return 'ندارد'
    calculate = calculatePrice(duration, price)
    if calculate is None: return '0'
    return f"{calculate:,.2f}"

@register.filter
def getlist(request, key):
    return request.getlist(key) if request and key else []

# New template tags for improved dashboard

@register.filter
def format_duration(duration):
    """Format duration in a more readable way"""
    if not duration or duration == '0:00' or duration == '0':
        return '00:00:00'

    s = str(duration).strip()
    if not any(ch.isdigit() for ch in s):
        return '00:00:00'

    s = s.replace("'", ":").replace('"', "")
    filtered = "".join(ch for ch in s if ch.isdigit() or ch == ":")
    if not filtered:
        return '00:00:00'

    try:
        parts = filtered.split(":")
        if len(parts) == 2:
            hours = '00'
            minutes, seconds = parts
        elif len(parts) == 3:
            hours, minutes, seconds = parts
        else:
            return '00:00:00'

        hours = hours.zfill(2)
        minutes = minutes.zfill(2)
        seconds = seconds.zfill(2)
        return f"{hours}:{minutes}:{seconds}"
    except Exception:
        return '00:00:00'

@register.filter
def format_phone_number(number):
    """Normalize phone number display to +98 format"""
    if not number:
        return ''
        
    # Clean the number
    number = str(number).replace(' ', '')
    
    # Normalize all formats to +98
    if number.startswith('+9800098'):
        # +9800098XXXXXXXXX → +98XXXXXXXXX (حذف 98000)
        number = '+98' + number[8:]
    elif number.startswith('+98000'):
        # +980009XXXXXXXXX → +989XXXXXXXXX (حذف 000)
        number = '+98' + number[6:]
    elif number.startswith('9800098'):
        # 9800098XXXXXXXXX → +98XXXXXXXXX
        number = '+98' + number[7:]
    elif number.startswith('98000'):
        # 980009XXXXXXXXX → +989XXXXXXXXX (حذف 000)
        number = '+98' + number[5:]
    elif number.startswith('+98'):
        # Already in +98 format, keep it
        pass
    elif number.startswith('0098'):
        # 00989XXXXXXXXX → +989XXXXXXXXX
        number = '+98' + number[4:]
    elif number.startswith('98') and len(number) >= 12:
        # 989XXXXXXXXX → +989XXXXXXXXX
        number = '+98' + number[2:]
    elif number.startswith('0') and len(number) >= 10:
        # 09XXXXXXXXX → +989XXXXXXXXX
        number = '+98' + number[1:]
    
    # Return the normalized number
    return number

@register.simple_tag
def is_active_filter(request, param, value):
    """Check if a filter is active"""
    values = request.GET.getlist(param)
    return 'bg-blue-100' if value in values else ''