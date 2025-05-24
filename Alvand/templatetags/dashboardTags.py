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
    
    try:
        # Try to parse the duration string
        if ':' in duration:
            parts = duration.split(':')
            if len(parts) == 2:
                minutes, seconds = parts
                hours = '00'
            elif len(parts) == 3:
                hours, minutes, seconds = parts
            else:
                return duration
                
            # Ensure each part has two digits
            hours = hours.zfill(2)
            minutes = minutes.zfill(2)
            seconds = seconds.zfill(2)
            
            return f"{hours}:{minutes}:{seconds}"
        else:
            return duration
    except:
        return duration

@register.filter
def format_phone_number(number):
    """Format phone number for better readability"""
    if not number:
        return ''
        
    # Clean the number
    number = str(number).replace(' ', '')
    
    # Check if it's an international number
    if number.startswith('+'):
        # Format international number
        if len(number) > 10:
            return f"{number[:4]} {number[4:7]} {number[7:10]} {number[10:]}"
        else:
            return number
    # Check if it's an extension
    elif len(number) <= 4 and number.isdigit():
        return number
    # Otherwise format as local number
    else:
        if len(number) >= 10:
            return f"{number[:3]} {number[3:6]} {number[6:8]} {number[8:]}"
        else:
            return number

@register.simple_tag
def is_active_filter(request, param, value):
    """Check if a filter is active"""
    values = request.GET.getlist(param)
    return 'bg-blue-100' if value in values else ''