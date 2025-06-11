import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .user_utils import getUserinfoByUsername, getTupleIndex
from django.views.generic import TemplateView, View, FormView
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from .forms import *
from .models import *
from functools import wraps
import math, jdatetime, wmi, pythoncom, random, os, sys
from django.db.models import Q
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db import models
from .models import Users
from .templatetags.userProfileTags import getListOfExtsGroups, getUserCanPerm, getUserInfo, getObjectOfInfo

upload = os.path.join("Alvand/static/upload")
os.makedirs(upload, exist_ok=True)

# Error data moved to setup_initial_data function to avoid DB access during module import

def setup_initial_data():
    # List of all error codes and their details
    errors = [
        (537, 'Change into Isolated mode', '• Malfunction occurred in Master unit or Backup Master unit.\n• Malfunction occurred in the communication path of Slave unit.', '• Check error log of Master unit or Backup Master unit.\n• Check all cable connections between the sites, and check that hubs, routers, etc. are operating correctly\n• Confirm that the communication transmission speed between sites is sufficient\n• Confirm that all other parties equipment is powered on\n• Consult your network administrator'),
        (538, 'Isolated mode was released', 'Isolated mode was released.', 'This message shows that the operation mode recovered from Isolated mode.'),
        (539, 'VPN error', 'A communication error is occurring in VPN.', '• Check all cable connections between PBX and the other equipment connected via VPN, and check that hubs, routers, etc. are operating correctly\n• Confirm that the communication transmission speed between PBX and the other equipment connected via VPN is sufficient\n• Confirm that all other parties equipment is powered on\n• Consult your network administrator'),
        (540, 'Network Security Alarm', 'Security issue such as DOS attacks occurred.', 'Consult your network administrator'),
        (541, 'NAS disconnected', '• NAS is not active\n• Network malfunction', '• Check all cable connections between the PBX and the NAS, and check that hubs, routers, etc. are operating correctly\n• Confirm that the communication transmission speed between the PBX and the NAS is sufficient\n• Confirm that all other equipment is powered on\n• Consult your network administrator'),
        (542, 'Not enough free space on NAS', '• Not enough memory space available to save the data\n• Wrong permission of the NAS', '• Remove unnecessary files from the NAS\n• Check the permission of the NAS')
    ]

    for error in errors:
        error_code_num, error_message, probable_cause, solution = error
        Errors.objects.get_or_create(
            errorcodenum=error_code_num,
            defaults={
                "errormessage": error_message,
                "probablecause": probable_cause,
                "solution": solution,
            },
        )

    telephones = [(1, None, 'آذربایجان', '+994', datetime.datetime(2025, 3, 6, 7, 58, 58, 880741, tzinfo=datetime.timezone.utc), None)]

    for item in telephones:
        _, type, name, code, _, _ = item
        
        Telephons.objects.get_or_create(
            code=code,
            defaults={
                'type': type,
                'name': name,
            }
        )

    get, created = Groups.objects.get_or_create(enname="supporter", pename="پشتیبانی")
    Groups.objects.get_or_create(enname="superadmin", pename="ابر مدیر")
    Groups.objects.get_or_create(enname="admin", pename="مدیر")
    Groups.objects.get_or_create(enname="member", pename="کاربر")

    getSup, createdSup = Users.objects.get_or_create(username="supporter", defaults={
        'password': make_password("DLqyS!5#dF13"),
        'group': get,
        'groupname': get.enname,
        'extension': -1,
        'lastname': 'الوند',
        'name': 'پشتیبانی',
        'email': 'erfanhosseyni54@gmail.com',
        'email_verified_at': timezone.now()
    })

    Infos.objects.get_or_create(user=getSup, defaults={
        'birthdate': '2025/03/25',
        'phonenumber': '09030435699',
        'telephone': '36057970',
        'province': '10',
        'city': 'مشهد',
        'address': 'فرهنگ',
        'gender': '2',
        'military': '4',
        'maritalstatus': '1',
        'educationdegree': '6',
        'educationfield': 'IoT',
        'cardnumber': '6104338908037191',
        'accountnumber': '1234567',
        'accountnumbershaba': '640120020000009520896080',
        'nationalcode': '1111111111'
    })

    Permissions.objects.get_or_create(user=getSup, defaults={
        'perm_email': True,
        'can_view': True,
        'can_write': True,
        'can_modify': True,
        'can_delete': True,
        'errorsreport': True
    })

def checkLicense():
    check = lices.objects.all()
    if check.exists() and not check.first().active:
        return False
    return True

def getVersion():
    ver = lices.objects.all()
    if not ver.exists(): return None
    return getTupleIndex(VERSIONS, ver.first().version)

def getInfosOfUserByUsername(username, value):
    if not username:
        return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists():
        return None
    infos = Infos.objects.filter(user=user.first())
    if not infos.exists(): return None
    if not value.lower() in [field.name for field in Infos._meta.fields]: return None
    return next(iter(infos.values(value).first().values()))

def getHWID():
    pythoncom.CoInitialize()
    system = wmi.WMI()
    return system.Win32_ComputerSystemProduct()[0].UUID if system else None


def validatePhotoExt(filename):
    try:
        name, ext = os.path.splitext(filename)
        if ext.lower() in [".png", ".jpg", ".jpeg"]:
            return ext
    except:
        return False


def isInternational(prefix):
    if Telephons.objects.filter(code__contains=prefix).exists():
        return True
    return False


def calculatePrice(duration: str, price: int) -> int:
    if not duration or price is None or price <= 0: return 0
    hour, minute, second = map(int, duration.split(":"))
    toSeconds = (hour * 3600) + (minute * 60) + second
    toMinutes = math.ceil(toSeconds / 60)
    return toMinutes * price


def persianCallTypeToEnglish(ct):
    callType = []
    if "همه تماس ها" in ct:
        return ['incomingNA', 'incomingRC', 'incomingAN', "Transfer", "incomingDISA", 'incomingHangUp', 'outGoing',
                'Extension']
    if "تماس های پاسخ نداده شده" in ct:
        if "incomingNA" not in callType: callType.append("incomingNA")
    if "تماس های ورودی" in ct:
        for item in ['incomingNA', 'incomingRC', 'incomingAN', "Transfer", "incomingDISA", 'incomingHangUp']:
            if item not in callType:
                callType.append(item)
    if "تماس های خروجی" in ct:
        if "outGoing" not in callType: callType.append("outGoing")
    if "تماس های داخلی" in ct:
        if "Extension" not in callType: callType.append("Extension")
    return callType


def getUrbanlinesThatUserAccessThem(username):
    if not username: return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return None
    allExts = []
    ext = user.first().extension
    if ext:
        allExts.append(ext)
    userexts = user.first().usersextension
    if userexts:
        for userext in userexts:
            if userext: allExts.append(userext)
    labels = Permissions.objects.filter(user=user.first())
    if labels.exists() and labels.first().exts_label:
        extgps = Extensionsgroups.objects.filter(label__in=labels.first().exts_label)
        if extgps.exists():
            for item in extgps:
                allExts = allExts + item.exts
    urbans = [x.urbanline for x in Records.objects.filter(extension__in=allExts) if x.urbanline]
    return sorted(set(urbans))

def getExtensionlines(username):
    if not username: return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return None
    allExtentions = []
    ext = user.first().extension
    if ext:
        allExtentions.append(ext)
    userexts = user.first().usersextension
    if userexts:
        for userext in userexts:
            if userext: allExtentions.append(userext)
    labels = Permissions.objects.filter(user=user.first())
    if labels.exists() and labels.first().exts_label:
        extGroup = Extensionsgroups.objects.filter(label__in=labels.first().exts_label)
        if extGroup.exists():
            for item in extGroup:
                allExtentions = allExtentions + item.exts
    extensions = [x.extension for x in Records.objects.filter(extension__in=allExtentions) if x.extension]
    return sorted(set(extensions))

def dashboardData(username):
    if not username: return []
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return []
    allExtentions = []
    ext = user.first().extension
    if ext:
        allExtentions.append(ext)
    userexts = user.first().usersextension
    if userexts:
        for userext in userexts:
            if userext: allExtentions.append(userext)
    labels = Permissions.objects.filter(user=user.first())
    if labels.exists() and labels.first().exts_label:
        extGroup = Extensionsgroups.objects.filter(label__in=labels.first().exts_label)
        if extGroup.exists():
            for item in extGroup:
                allExtentions = allExtentions + item.exts
    extensions = [x for x in Records.objects.filter(extension__in=allExtentions).order_by('-created_at')]
    return extensions

def getPrice(which):
    if not which: return None
    price = None
    cost = Costs.objects.all()
    match which.lower():
        case "irancell":
            if cost.exists():
                price = cost.first().irancell
        case "hamrahaval":
            if cost.exists():
                price = cost.first().hamrahaval
        case "rightel":
            if cost.exists():
                price = cost.first().rightel
        case "provincial":
            if cost.exists():
                price = cost.first().provincial
        case "international":
            if cost.exists():
                price = cost.first().international
        case "outofprovincial":
            if cost.exists():
                price = cost.first().outofprovincial
        case _:
            return None
    if not price: return None
    return price


def callTypeDetector(number):
    number = str(number)
    if len(number) < 5:
        return None
    if number[0:3] == "+98":
        number = number.replace("+98", "0")
    if number[0:3] == "000":
        number = number[3:]
    if number[0:2] == "98":
        if number[2:4] != "09":
            number = "09" + number[4:]
        else:
            number = "0" + number[2:]
    if number[0:4] == "0098":
        number = "0" + number[4:]
    hamrahaval = ["0910", "0910", "0912", "0913", "0914", "0915", "0916", "0917", "0918", "0919", "0991", "0990",
                  "0992", "0993", "0996"]
    irancell = ["0900", "0901", "0902", "0903", "0904", "0905", "0930", "0933", "0935", "0936", "0937", "0938", "0939",
                "0941"]
    rightel = ["0921", "0922", "0923", "0920"]
    outofprovincial = ["041", "044", "045", "031", "084", "077", "021", "038", "051", "056", "058", "061", "024", "023",
                       "054", "071", "026", "025", "028", "087", "034", "083", "074", "017", "013", "066", "011", "086",
                       "076", "081", "035"]
    return "irancell" if number[0:4] in irancell else "hamrahaval" if number[
                                                                      0:4] in hamrahaval else "rightel" if number[
                                                                                                           0:4] in rightel else "international" if isInternational(
        number[0:3]) else "provincial" if int(number[0]) in range(1, 9) else "outofprovincial" if number[
                                                                                                  0:3] in outofprovincial else None


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


def getRandomCode():
    rand = random.randint(100000, 999999)
    if not Verifications.objects.filter(code=rand).exists():
        return rand
    getRandomCode()


def makePagination(objs, itemsPerPage, request):
    paginator = Paginator(objs, itemsPerPage)
    page = request.GET.get('p', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj.object_list, page_obj


def getInfosOfUserByUsername(username, value):
    if not username:
        return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists():
        return None
    infos = Infos.objects.filter(user=user.first())
    if not infos.exists(): return None
    if not value.lower() in [field.name for field in Infos._meta.fields]: return None
    return next(iter(infos.values(value).first().values()))


def sendEmail(subject: str, message: str, recipients: list, request) -> bool:
    try:
        emailInfo = Emailsending.objects.all()
        if not emailInfo.exists():
            return None
        username, password = emailInfo.values('collectionusername', 'collectionpassword').first().values()
        f = open("Alvand/templates/email-temp.html", 'r', encoding='utf-8')
        msg = f.read()
        msg = msg.replace("{{ message }}", message)
        return send_mail(subject, message, recipient_list=recipients, html_message=msg, from_email=username,
                         auth_user=username, auth_password=password) > 0
    except Exception as err:
        errMsg = None
        if isinstance(err.args[0], bytes) and "invalid address" in err.args[0].decode().lower():
            errMsg = f"آدرس ارسال شده برای ارسال ایمیل نامعتبر می باشد ({err.args[0].lower().replace("invalid address ", "").replace('"', "")})"
        else:
            if isinstance(err.args[1], bytes) and "username and password not accepted. for more information" in \
                    err.args[1].decode().lower():
                errMsg = f"نام کاربری و رمز عبور برای ارسال ایمیل نامعتبر است\nلطفا با مدیریت خود جهت تصحیح نام کاربری و رمز عبور در ارتباط باشید."
        log(request, logErrCodes.emails, logMessages.emailCouldnotSend.format(err, ))
        return errMsg or False


def hasAccess(access, redirectTo=None, request=None):
    if request:
        res = _check_access(access, redirectTo, request)
        if isinstance(res, HttpResponseRedirect):
            return res
        return True

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(self, request, *args, **kwargs):
            res = _check_access(access, redirectTo, request)
            if isinstance(res, HttpResponseRedirect):
                return res
            return view_func(self, request, *args, **kwargs)

        return wrapped_view

    return decorator


def _check_access(access, redirectTo, request):
    username = checkSession(request)
    if not username:
        messages.error(request, messagesTypes.notlogin)
        return redirect(reverse_lazy("login"))

    user = Users.objects.filter(username__iexact=username)
    if not user.exists():
        messages.error(request, messagesTypes.userInfoNotFound)
        return redirect(reverse_lazy("login"))

    perm = Permissions.objects.filter(user=user.first())
    if not perm.exists():
        messages.error(request, messagesTypes.permissionsNotFound)
        return redirect(reverse_lazy("dashboard" if not redirectTo else redirectTo))

    if access.lower() not in ['view', 'write', 'modify', 'delete']:
        messages.error(request, messagesTypes.permissionsTypeNotFound)
        return redirect(reverse_lazy("dashboard" if not redirectTo else redirectTo))

    if user.first().groupname.lower() == "member":
        messages.error(request, messagesTypes.accessDeniedUser)
        return redirect(reverse_lazy("dashboard" if not redirectTo else redirectTo))

    can_access = perm.values(f'can_{access.lower()}').first()
    if not can_access or not can_access[f'can_{access.lower()}']:
        messages.error(request, messagesTypes.accessDeniedView if access.lower() == "view" else
        messagesTypes.accessDeniedWrite if access.lower() == "write" else
        messagesTypes.accessDeniedModify if access.lower() == "modify" else
        messagesTypes.accessDeniedDelete)
        return redirect(reverse_lazy("dashboard" if not redirectTo else redirectTo))

    return True

def check_active(username):
    active = Users.objects.filter(username__iexact=username)
    if active.exists():
        return active.first().active
    return False

def check_groupname(groupname):
    if groupname.lower() == 'user':
        return 'admin'
    elif groupname.lower() == 'admin':
        return 'superadmin'
    elif groupname.lower() == 'superadmin':
        return 'supporter'
    elif groupname.lower() == 'supporter':
        return 'supporter'
    else:
        return None

def getVersion():
    ver = lices.objects.all()
    if not ver.exists():return None
    return getTupleIndex(VERSIONS, ver.first().version)

def systemSettingsConfiguration(field, fieldRequest, request, success_url, form, isEthernet):

    if not isEthernet:
        if not field.get('device'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('flow'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('stopbits'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('baudrate'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('parity'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('databits'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('number_of_lines'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)

        if field.get('device') not in ['KX-TA308', 'KX-TES824', 'KX-TEM824']:
            messages.error(request, messagesTypes.fillNotInFields.format('تنطیمات دستگاه', ))
            return redirect(success_url)
        if field.get('flow') not in ['None', 'XON/XOFF', 'RTS/CTS', 'DSR/DTR']:
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if field.get('stopbits') not in [1, 1.5, 2]:
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if field.get('baudrate') not in [4800, 9600, 19200, 38400, 57600, 112500, 230400, 460800,
                                            921600]:
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if field.get('parity') not in ['None', 'Odd', 'Even', 'Mark', 'Space']:
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if field.get('databits') not in [5, 6, 7, 8]:
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('number_of_lines').isdigit():
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)

        dev = Device.objects.all()
        if dev.exists():
            dev.update(device=field.get('device'), flow=field.get('flow'), stopbits=field.get('stopbits'),
                        baudrate=field.get('baudrate'),
                        parity=field.get('parity'), databits=field.get('databits'),
                        number_of_lines=field.get('number_of_lines'))
            log(request, logErrCodes.systemSettings, logMessages.updatedSettings.format('تنظیمات دستگاه'),
                checkSession(request))
        else:
            form.save()
            log(request, logErrCodes.systemSettings, logMessages.createdSettings.format('تنظیمات دستگاه'),
                checkSession(request))
    else:
        if not field.get('device'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('smdrip'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('smdrport'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('smdrpassword'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('number_of_lines'):
            messages.error(request, messagesTypes.fillAllFieldsInSection.format('تنظیمات دستگاه', ))
            return redirect(success_url)

        if field.get('device') not in ['KX-NS300', 'KX-NS500', 'KX-NS700', 'KX-NS1000', 'KX-HTS32', 'KX-HTS824']:
            messages.error(request, messagesTypes.fillNotInFields.format('تنطیمات دستگاه', ))
            return redirect(success_url)
        if not any( x.isdigit() for x in field.get('smdrip').split('.')):
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('smdrport').isdigit():
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)
        if not field.get('number_of_lines').isdigit():
            messages.error(request, messagesTypes.fillNotInFields.format('تنظیمات دستگاه', ))
            return redirect(success_url)


        dev = Device.objects.all()
        if dev.exists():
            dev.update(device=field.get('device'), flow=None, stopbits=None,
                        baudrate=None,
                        parity=None, databits=None,
                        number_of_lines=field.get('number_of_lines'), smdrip=field.get('smdrip'), smdrport=field.get('smdrport'), smdrpassword=field.get('smdrpassword'))
            log(request, logErrCodes.systemSettings, logMessages.updatedSettings.format('تنظیمات دستگاه'),
                checkSession(request))
        else:
            form.save()
            log(request, logErrCodes.systemSettings, logMessages.createdSettings.format('تنظیمات دستگاه'),
                checkSession(request))

    return "تنظیمات دستگاه\n"



class verificationType:
    email = 0
    phone = 1


class messagesTypes:
    notlogin = "شما هنوز وارد حساب کاربری خود نشده اید."
    login = "کاربر {}، به حساب خود خوش آمدید"
    loggedIn = "شما از قبل وارد حساب خود شده اید."
    logout = "شما با موفقیت از حساب خود خارج شدید."
    invalidUsernameOrPassword = 'رمز عبور و یا نام کاربری نا معتبر است.'
    userInfoNotFound = "مشخصات کاربری شما یافت نشد."
    permissionsNotFound = "دسترسی یافت نشد."
    permissionsTypeNotFound = "نوع دسترسی نامعتبر است."
    accessDeniedUser = "شما مجاز به اقدام/انجام عملیات در قسمت های مدیریتی نیستید."
    accessDeniedView = "شما دسترسی دیدن این قسمت را ندارید."
    accessDeniedWrite = "شما دسترسی ایجاد کردن در این قسمت را ندارید."
    accessDeniedModify = "شما دسترسی ویرایش کردن در این قسمت را ندارید."
    accessDeniedDelete = "شما دسترسی حذف کردن در این قسمت را ندارید."
    fillAllFields = "لطفا تمامی مقادیر را کامل نمایید."
    fillAllFieldsInSection = "لطفا تمامی مقادیر را در {} کامل کنید."
    fillNotInFields = "مقدار انتخاب شده شما در {} نامعتبر است."
    licenseExpiredOrNotValid = "اعتبار لایسنس شما منقضی و یا معتبر نمی باشد."
    deAvtive = "حساب شما غیرفعال است"


class logErrCodes:
    logInOut = 0x21F1  # Login and logout
    emails = 0x211F  # Emails
    userSettings = 0x3F2  # User Settings
    systemSettings = 0x3F3  # System Settings
    license = 0x4F1
    others = 0xFFF0


class logMessages:
    loggedIn = "کاربر {} وارد حساب خود شد."
    loggedOut = "کاربر {} از حساب خود خارج شد."
    userProcessEmail = "کاربر {} اقدام به تایید ایمیل خود کرد"
    emailVerifyCodeSent = "کد با موفقیت برای کاربر {} با ایمیل {} ارسال شد."
    emailVerified = "ایمیل کاربر {} با موفقیت تایید شد."
    emailCouldnotSend = "ارسال ایمیل با خطا مواجه شد. ({})"
    createdSettings = "{} با موفقیت ثبت شد."
    updatedSettings = "{} با موفقیت بروزرسانی شد."
    dataDidnotSend = "داده ها ارسال نشد."
    dataSent = "داده ها با موفقیت ارسال شد."
    licenseExp = messagesTypes.licenseExpiredOrNotValid


def home(request):
    # Call setup_initial_data on first access to initialize the database
    setup_initial_data()
    return redirect('/dashboard')

def licenseNotActive(request):
    return render(request, "license.html", context={'pageTitle': 'لایسنس شما فعال نمی باشد', "hwid": getHWID()})

class systemSettings(FormView, View):
    template_name = 'settings.html'
    model = Device
    form_class = DeviceForm
    success_url = reverse_lazy('settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = 'تنظیمات سیستمی'
        context["deviceform"] = self.form_class
        context["contactInfo"] = ContactInfoForm()
        context['costForm'] = costsForm()
        context["extGroup"] = extGroups()
        context["groupname"] = Extensionsgroups.objects.all()
        context['emailSendingForm'] = emailSendingForm()
        context['userAccessToErrorsPageForm'] = userAccessToErrorsPageForm()
        context['users'] = Users.objects.exclude(groupname__in=['superadmin', 'supporter'])
        context['errors'] = Emailsending.objects.all().first().errors if Emailsending.objects.all().exists() else None
        context['emailset'] = Emailsending.objects.all() if Emailsending.objects.all().exists() else None
        context['contactInfos'] = ContactInfo.objects.all() if ContactInfo.objects.all().exists() else None
        context['devices'] = Device.objects.all() if Device.objects.all().exists() else None
        context['costs'] = Costs.objects.all() if Costs.objects.all().exists() else None
        context['version'] = getVersion()
        return context

    @hasAccess('view')
    def get(self, request, *args, **kwargs):
        if not checkSession(self.request):
            messages.error(self.request, messagesTypes.notlogin)
            return redirect(reverse_lazy('login'))
        if not check_active(checkSession(request)):
            messages.error(request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def form_valid(self, form):
        if not checkSession(self.request):
            messages.error(self.request, messagesTypes.notlogin)
            return redirect(reverse_lazy('login'))
        if not check_active(checkSession(self.request)):
            messages.error(self.request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(self.request) else 'login'))
        if isinstance(check := hasAccess("view", "settings", self.request), HttpResponseRedirect):
            return check
        if isinstance(check := hasAccess("write", "settings", self.request), HttpResponseRedirect):
            return check
        if isinstance(check := hasAccess("modify", "settings", self.request), HttpResponseRedirect):
            return check
        msgs = "تنظیمات زیر با موفقیت ذخیره شد:\n"
        field = form.cleaned_data
        fieldRequest = self.request.POST
        if any(f for f in [field.get('device'), field.get('flow'), field.get('stopbits'), field.get('baudrate'),
                            field.get('parity'), field.get('databits'), field.get('number_of_lines')]) or any (f for f in [field.get('smdrip'),
                            field.get('smdrport'), field.get('smdrpassword')]):
            if getVersion() == 'alvand':
                systemSettingsConfiguration(field, fieldRequest, self.request, self.success_url, form, False)
            elif getVersion == 'binalud':
                isEthernet = False
                if field.get('device') in ['KX-TDA30','KX-TDA100','KX-TDA100D','KX-TDA100DBA','KX-TDA200','KX-TDA600']:
                    isEthernet = False
                elif field.get('device') in ['KX-NS300', 'KX-NS500', 'KX-NS700', 'KX-NS1000', 'KX-HTS32', 'KX-HTS824']:
                    isEthernet = True
                else:
                    cable = field.get('cable_type')
                    if not cable or cable.lower() == 'none':
                        messages.error(self.request, 'لطفا یکی از انواع کابل هارا انتخاب کنید.')
                        return redirect(self.success_url)
                    elif cable.lower() == 'rs232c':
                        isEthernet = False
                    else:
                        isEthernet = True

                systemSettingsConfiguration(field, fieldRequest, self.request, self.success_url, form, isEthernet)

            else:
                messages.error(self.request, 'نسخه برنامه شما هنوز مشخص نشده است.')
                return redirect(self.success_url)

        if any(f for f in [fieldRequest.get('province'), fieldRequest.get('phone_number')]):
            if not fieldRequest.get('province'):
                messages.error(self.request, messagesTypes.fillAllFieldsInSection.format('اطلاعات تماس'))
                return redirect(self.success_url)
            if not fieldRequest.get('phone_number'):
                messages.error(self.request, messagesTypes.fillAllFieldsInSection.format('اطلاعات تماس'))
                return redirect(self.success_url)
            if not fieldRequest.get('province').isdigit():
                messages.error(self.request, messagesTypes.fillNotInFields.format('انتخاب استان'))
                return redirect(self.success_url)
            if fieldRequest.get('province') not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']:
                messages.error(self.request, messagesTypes.fillNotInFields.format('انتخاب استان'))
                return redirect(self.success_url)
            if not fieldRequest.get('phone_number').isdigit():
                messages.error(self.request, messagesTypes.fillNotInFields.format('شماره همراه مدیر'))
                return redirect(self.success_url)
            if len(fieldRequest.get('phone_number')) != 11:
                messages.error(self.request, messagesTypes.fillNotInFields.format('شماره همراه مدیر'))
                return redirect(self.success_url)

            conInfo = ContactInfo.objects.all()
            if conInfo.exists():
                conInfo.update(province=fieldRequest.get('province'), phone_number=fieldRequest.get('phone_number'),
                               user=Users.objects.filter(username__iexact=checkSession(self.request)).first())
                log(self.request, logErrCodes.systemSettings, logMessages.updatedSettings.format('اطلاعات تماس'),
                    checkSession(self.request))

            else:
                ContactInfo.objects.create(province=fieldRequest.get('province'),
                                           phone_number=fieldRequest.get('phone_number'), user=Users.objects.filter(
                        username__iexact=checkSession(self.request)).first())
                log(self.request, logErrCodes.systemSettings, logMessages.createdSettings.format('اطلاعات تماس'),
                    checkSession(self.request))
            msgs += "اطلاعات تماس\n"
        if fieldRequest.get('edit') or fieldRequest.get('delete') or fieldRequest.get('add'):
            editext = Extensionsgroups.objects.filter(label__iexact=fieldRequest.get('label'))

            if not any(f for f in [any(x for x in fieldRequest.getlist('exts')), fieldRequest.get('label')]):
                messages.error(self.request, messagesTypes.fillAllFields)
                return redirect(self.success_url)
            if fieldRequest.get('edit'):
                if not editext.exists():
                    messages.error(self.request, 'این نام گروه وجود ندارد.')
                    return redirect(self.success_url)
                getExtFromDB = editext.values_list('exts', flat=True).first() or []
                valuesFromUser = [int(x) for x in fieldRequest.getlist('exts')]
                mightRemove = set(getExtFromDB) - set(valuesFromUser)
                mightAdd = set(valuesFromUser) - set(getExtFromDB)
                mergeAndUpdate = list((set(getExtFromDB) - mightRemove) | mightAdd)
                editext.update(exts=mergeAndUpdate, label=fieldRequest.get('label'),
                               modifyby=Users.objects.filter(username__iexact=checkSession(self.request)).first())
                msgs += "ویرایش تنظیمات دسترسی به گروه ها\n"

            if fieldRequest.get('add'):
                if editext.exists():
                    messages.error(self.request, 'این نام گروه وجود دارد.')
                    return redirect(self.success_url)
                if len(fieldRequest.get('label')) <= 3 and len(fieldRequest.get('label')) >= 25:
                    messages.error(self.request, 'نام گروه باید بین ۳ تا ۲۵ حرف باشد.')
                    return redirect(self.success_url)

                Extensionsgroups.objects.create(label=fieldRequest.get('label'),
                                                exts=[int(x) for x in fieldRequest.getlist('exts')],
                                                modifyby=Users.objects.filter(
                                                    username__iexact=checkSession(self.request)).first())
                msgs += "اضافه تنظیمات دسترسی به گروه ها\n"
            if fieldRequest.get('delete'):
                lbl = fieldRequest.get('label')
                editext = Extensionsgroups.objects.filter(label__iexact=lbl)
                if not editext.exists():
                    messages.error(self.request, 'این نام گروه وجود ندارد.')
                    return redirect(self.success_url)
                perms = Permissions.objects.filter(exts_label__contains=[lbl])
                if perms.exists():
                    for perm in perms:
                        if lbl in perm.exts_label:
                            updateLbl = [label for label in perm.exts_label if label != lbl]
                            perm.exts_label = updateLbl
                            perm.save()
                editext.delete()
                msgs += f"حذف گروه {lbl} از تنظیمات دسترسی به گروه ها\n"

        if any(cost for cost in
               [fieldRequest.get("hamrahaval"), fieldRequest.get("irancell"), fieldRequest.get("rightel"),
                fieldRequest.get("provincial"), fieldRequest.get("international"),
                fieldRequest.get("outofprovincial")]):
            if not fieldRequest.get("hamrahaval") or not fieldRequest.get("irancell") or not fieldRequest.get(
                    "rightel") or not fieldRequest.get("provincial") or not fieldRequest.get(
                "international") or not fieldRequest.get("outofprovincial"):
                messages.error(self.request, messagesTypes.fillAllFieldsInSection.format('هزینه های تماس'))
                return redirect(self.success_url)
            fields = [fieldRequest.get("hamrahaval"), fieldRequest.get("irancell"), fieldRequest.get("rightel"),
                      fieldRequest.get("provincial"), fieldRequest.get("international"),
                      fieldRequest.get("outofprovincial")]
            if any(not isfloat(item) for item in fields):
                messages.error(self.request, "لطفا مقادیر هزینه های تماس را به صورت اعشار و یا عدد صحیح بنویسید.")
                return redirect(self.success_url)
            if any(float(item) < 0.0 for item in fields):
                messages.error(self.request, "هزینه های تماس نباید کمتر از 0 باشد.")
                return redirect(self.success_url)
            costs = Costs.objects
            if costs.all().exists():
                costs.update(hamrahaval=fieldRequest.get('hamrahaval'), irancell=fieldRequest.get('irancell'),
                             rightel=fieldRequest.get('rightel'),
                             provincial=fieldRequest.get('provincial'), international=fieldRequest.get('international'),
                             outofprovincial=fieldRequest.get('outofprovincial'), updated_at=timezone.now())
                log(self.request, logErrCodes.systemSettings, logMessages.updatedSettings.format('هزینه های تماس'),
                    checkSession(self.request))
            else:
                costs.create(hamrahaval=fieldRequest.get('hamrahaval'), irancell=fieldRequest.get('irancell'),
                             rightel=fieldRequest.get('rightel'),
                             provincial=fieldRequest.get('provincial'), international=fieldRequest.get('international'),
                             outofprovincial=fieldRequest.get('outofprovincial'), created_at=timezone.now())
                log(self.request, logErrCodes.systemSettings, logMessages.createdSettings.format('هزینه های تماس'),
                    checkSession(self.request))
            msgs += "هزینه های تماس\n"
        if any(f for f in [fieldRequest.get('collectionusername'), fieldRequest.get('collectionpassword'),
                           fieldRequest.get('emailtosend'), any(err for err in fieldRequest.getlist('errors'))]):
            if not all(f for f in [fieldRequest.get('collectionusername'), fieldRequest.get('collectionpassword'),
                                   fieldRequest.get('emailtosend'),
                                   any(err for err in fieldRequest.getlist('errors'))]):
                messages.error(self.request, messagesTypes.fillAllFieldsInSection.format('تنظیمات ایمیل'))
                return redirect(self.success_url)
            if not all("@gmail.com" in x.strip() for x in
                       [fieldRequest.get('collectionusername'), fieldRequest.get('emailtosend')]):
                messages.error(self.request, "ایمیل باید حتما دارای @gmail.com باشد. (مانند example@gmail.com)")
                return redirect(self.success_url)
            if any(len(x.strip().replace("@gmail.com", "")) < 3 for x in
                   [fieldRequest.get('collectionusername'), fieldRequest.get('emailtosend')]):
                messages.error(self.request, "ایمیل وارد شده نامعتبر است.")
                return redirect(self.success_url)
            if not fieldRequest.get('lines').isdigit() and not int(fieldRequest.get('lines')) in range(1, 10 + 1):
                messages.error(self.request, messagesTypes.fillNotInFields.format('تعداد خطاها برای ارسال'))
                return redirect(self.success_url)
            if not any(item.isdigit() for item in fieldRequest.getlist('errors')):
                messages.error(self.request, messagesTypes.fillNotInFields.format('خطاها'))
                return redirect(self.success_url)
            if not any(
                    Errors.objects.filter(errorcodenum=int(item)).exists() for item in fieldRequest.getlist('errors')):
                messages.error(self.request, "یکی از خطا های انتخاب شده وجود ندارد.")
                return redirect(self.success_url)
            emailSendCheck = Emailsending.objects
            if emailSendCheck.all().exists():
                emailSendCheck.update(errors=[int(x) for x in fieldRequest.getlist('errors')],
                                      emailtosend=fieldRequest.get('emailtosend'),
                                      collectionusername=fieldRequest.get('collectionusername'),
                                      collectionpassword=fieldRequest.get('collectionpassword'),
                                      lines=int(fieldRequest.get('lines')),
                                      byadmin=Users.objects.filter(username__iexact=checkSession(self.request)).first(),
                                      updated_at=timezone.now())
                log(self.request, logErrCodes.systemSettings, logMessages.updatedSettings.format('تنظیمات ایمیل'),
                    checkSession(self.request))

            else:
                emailSendCheck.create(errors=[int(x) for x in fieldRequest.getlist('errors')],
                                      emailtosend=fieldRequest.get('emailtosend'),
                                      collectionusername=fieldRequest.get('collectionusername'),
                                      collectionpassword=fieldRequest.get('collectionpassword'),
                                      lines=int(fieldRequest.get('lines')),
                                      byadmin=Users.objects.filter(username__iexact=checkSession(self.request)).first(),
                                      created_at=timezone.now())
                log(self.request, logErrCodes.systemSettings, logMessages.createdSettings.format('تنظیمات ایمیل'),
                    checkSession(self.request))
            msgs += "تنظیمات ایمیل\n"
        if fieldRequest.get('users') and fieldRequest.get("users").lower() != "none":
            user = Users.objects.filter(username__iexact=fieldRequest.get('users'))
            if not user.exists():
                messages.error(self.request, f"کاربر {fieldRequest.get('users')} وجود ندارد.")
                return redirect(self.success_url)
            perm = Permissions.objects.filter(user=user.first())
            if not perm.exists():
                Permissions.objects.create(user=user.first(), errorsreport=bool(fieldRequest.get('errorsreport')))
            else:
                perm.update(errorsreport=bool(fieldRequest.get('errorsreport')))
            log(self.request, logErrCodes.systemSettings,
                logMessages.updatedSettings.format('دسترسی به گزارش خطا ها - گروه بندی دسترسی ها'),
                checkSession(self.request))
            msgs += "دسترسی به گزارش خطا ها - گروه بندی دسترسی ها\n"
        if msgs != "تنظیمات زیر با موفقیت ذخیره شد:\n":
            messages.success(self.request, msgs)
        else:
            messages.info(self.request, "هیچ تغییراتی اعمال نشده است.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        if not checkSession(self.request):
            messages.error(self.request, messagesTypes.notlogin)
            return redirect(self.success_url)
        if not check_active(checkSession(self.request)):
            messages.error(self.request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(self.request) else 'login'))
        if isinstance(check := hasAccess("write", "user", self.request), HttpResponseRedirect):
            return check
        messages.error(self.request, messagesTypes.fillAllFields)
        return redirect(self.success_url)


class dashboardPage(TemplateView, View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        if not checkSession(request):
            messages.error(request, messagesTypes.notlogin)
            return redirect(reverse_lazy("login"))
        if not check_active(checkSession(request)):
            messages.error(request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
        context = self.get_context_data()
        if request.GET:
            dateFrom = request.GET.get('dateFrom')
            dateTo = request.GET.get('dateTo')
            urbanline = request.GET.getlist('urbanline')
            extline = request.GET.getlist('extline')
            calls = request.GET.getlist('calls')
            calls = persianCallTypeToEnglish(calls) if calls else None
            calltype = Q(calltype__in=calls) if calls else Q()
            urbanline = Q(urbanline__in=urbanline) if urbanline and "همه تماس ها" not in request.GET.getlist(
                'calls') else Q()
            extline = Q(extension__in=extline) if extline and "همه تماس ها" not in request.GET.getlist('calls') else Q()
            filterDate = None
            if dateFrom and dateTo:
                try:
                    convFrom = jdatetime.datetime.strptime(dateFrom.replace("/", "-").replace('از', '').strip(), "%Y-%m-%d").togregorian()
                    convTo = jdatetime.datetime.strptime(dateTo.replace("/", "-").replace('تا', '').strip(), "%Y-%m-%d").togregorian()
                except:
                    messages.error(request, "فرمت تاریخ ها اشتباه است.")
                    return redirect(request.path)
                if convTo < convFrom:
                    messages.warning(request, "تاریخ اول نباید بزرگ تر از تاریخ دوم باشد.")
                    return redirect(request.path)

                filterDate = Q(date__range=(convFrom, convTo))
            query = Q()
            if urbanline:
                query &= urbanline
            if calltype:
                query &= calltype
            if extline:
                query &= extline
            if filterDate:
                query &= filterDate
            faults, page_obj = makePagination(
                Records.objects.filter(query).order_by(
                    '-created_at') if any(
                    item for item in [urbanline, calltype, extline, filterDate]) else dashboardData(
                    checkSession(request)), 20, request)
            context['dashPage'] = page_obj
        return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'داشبورد'
        faults, page_obj = makePagination(dashboardData(checkSession(self.request)), 20, self.request)
        context['dashPage'] = page_obj
        context['urbanlines'] = getUrbanlinesThatUserAccessThem(checkSession(self.request))
        context['extlines'] = getExtensionlines(checkSession(self.request))
        return context


def support(request):
    return render(request, 'support.html', context={'pageTitle': 'پشتیبانی'})


def checkSession(request):
    if 'user' in request.session:
        return request.session['user']
    return False


def login(request, user):
    if 'user' not in request.session:
        request.session['user'] = user.lower()
        return request.session['user']
    return request.session['user']


def getIPAddress(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log(request, errCode, errMessage, byWho=None):
    user = Users.objects.filter(username__iexact=checkSession(request) if not isinstance(request, str) else request)
    if not user.exists():
        return False
    ip = getIPAddress(request)
    return bool(
        Log.objects.create(user=user.first(), userBackup=user.first().username, errCode=errCode, errMessage=errMessage,
                           byWho=byWho if byWho else "Lotus", ip=ip,
                           macAddress=getInfosOfUserByUsername(user.first().username, 'macaddress')))


class logout(TemplateView):
    def get(self, request, *args, **kwargs):
        if checkSession(request):
            log(request, logErrCodes.logInOut, logMessages.loggedOut.format(request.session['user'], ),
                request.session['user'])
            del request.session['user']
            messages.success(request, messagesTypes.logout)
        else:
            messages.error(request, messagesTypes.notlogin)
        return redirect(reverse_lazy('login'))


class Profile(TemplateView, View):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = "پروفایل کاربری"
        user = Users.objects.filter(username__iexact=str(checkSession(self.request)))
        context['user'] = user.first() if user.exists() else None
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not checkSession(request):
            messages.warning(request, messagesTypes.userInfoNotFound)
            return redirect(reverse_lazy("login"))
        if not check_active(checkSession(request)):
            messages.error(request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
        if not Users.objects.filter(username__iexact=checkSession(request)).first().email_verified_at:
            if Verifications.objects.filter(user=Users.objects.filter(username__iexact=checkSession(request)).first(),
                                            type=verificationType.email).exists():
                context['email'] = True
        else:
            if 'email' in context: del context['email']
        return render(request, self.template_name, context=context)

    def post(self, request):
        if not checkSession(request):
            messages.error(request, messagesTypes.notlogin)
            return redirect(reverse_lazy("login"))
        if not check_active(checkSession(request)):
            messages.error(request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
        
        # Handle profile picture upload
        if request.POST.get('action') == 'upload_profile_pic' and request.FILES.get('profile_picture'):
            try:
                import os
                from django.conf import settings
                import json
                from django.http import JsonResponse
                
                user = Users.objects.filter(username__iexact=checkSession(request)).first()
                if not user:
                    return JsonResponse({'success': False, 'error': 'کاربر یافت نشد'})
                
                profile_pic = request.FILES['profile_picture']
                
                # Validate file type
                valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                ext = os.path.splitext(profile_pic.name)[1].lower()
                if ext not in valid_extensions:
                    return JsonResponse({'success': False, 'error': 'فرمت فایل نامعتبر است. فقط jpg, jpeg, png, gif و webp مجاز هستند.'})
                
                # Validate file size (max 2MB)
                if profile_pic.size > 2 * 1024 * 1024:
                    return JsonResponse({'success': False, 'error': 'حجم فایل باید کمتر از 2 مگابایت باشد'})
                
                # Create directory if it doesn't exist
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                # Generate filename based on username to avoid duplicates
                filename = f"{user.username}{ext}"
                filepath = os.path.join(upload_dir, filename)
                
                # Delete old profile picture if exists
                if user.profile_picture and os.path.exists(os.path.join(settings.MEDIA_ROOT, user.profile_picture)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, user.profile_picture))
                
                # Save the new profile picture
                with open(filepath, 'wb+') as destination:
                    for chunk in profile_pic.chunks():
                        destination.write(chunk)
                
                # Update user model
                relative_path = os.path.join('profile_pics', filename)
                user.profile_picture = relative_path
                user.save()
                
                # Log the action
                log(request, logErrCodes.userSettings, f"کاربر {user.username} تصویر پروفایل خود را بروزرسانی کرد", user.username)
                
                # Return success response with image URL
                image_url = os.path.join(settings.MEDIA_URL, relative_path)
                return JsonResponse({'success': True, 'image_url': image_url})
                
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        
        email = getUserinfoByUsername("email")
        user = Users.objects.filter(email__iexact=email)
        verEmail = request.POST.get("verifyEmail")
        resend = request.POST.get("resend")
        if verEmail or resend:
            context = self.get_context_data()
            if not email:
                messages.error(request, messagesTypes.userInfoNotFound)
                return redirect(reverse_lazy("profile"))
            if not user.exists():
                messages.error(request, messagesTypes.userInfoNotFound)
                return redirect(reverse_lazy("profile"))
            if user.first().email_verified_at:
                messages.error(request, "ایمیل شما از قبل تایید شده است.")
                return redirect(reverse_lazy("profile"))
            verModel = Verifications.objects.filter(type=verificationType.email, user=user.first())
            if verEmail and not resend:
                if verModel.exists():
                    context['email'] = True
                    messages.error(request, "کد تاییدیه ایمیل از قبل برای شما ارسال شده است.")
                    return render(request, self.template_name, context=context)
            elif not verEmail and resend:
                if not verModel.exists():
                    if 'email' in context:
                        del context['email']
                    messages.error(request, "شما هیچ فرایند تاییدیه ایمیلی ندارید.")
                    return render(request, self.template_name, context=context)
            rand = getRandomCode()
            sent = sendEmail("تاییدیه ایمیل", f"code: {rand}", [email], request=request)
            if sent is True:
                if verEmail and not resend:
                    Verifications.objects.create(type=verificationType.email,
                                                 user=user.first(), code=rand)
                    log(request, logErrCodes.emails, logMessages.userProcessEmail.format(user.first().username, ),
                        user.first().username)
                elif not verEmail and resend:
                    verModel.update(code=rand)
                log(request, logErrCodes.emails,
                    logMessages.emailVerifyCodeSent.format(user.first().username.capitalize(), email.capitalize()),
                    user.first().username)
                context['email'] = True
                messages.success(request,
                                 f"کد تاییدیه {'مجددا' if not verEmail and resend else ''} به ایمیل شما ارسال شد.\nتوجه داشته باشید که حتما پوشه اسپم چک شود.")
                return render(request, self.template_name, context=context)
            elif sent is not True and sent is not False:
                messages.error(request, sent)
            messages.error(request, "در ارسال ایمیل با مشکلی مواجه شده ایم\nلطفا با مدیر خود در ارتباط باشید.")
        verifyBtn = request.POST.get("verify")
        if verifyBtn:
            code = request.POST.get("code")
            if not user.exists():
                messages.error(request, messagesTypes.userInfoNotFound)
                return redirect(reverse_lazy("profile"))
            if not user.first().email_verified_at:
                messages.error(request, "ایمیل شما از قبل تایید شده است.")
                return redirect(reverse_lazy("profile"))
            context = self.get_context_data()
            if not code.isdigit():
                context['email'] = True
                messages.error(request, "کد وارد شده نامعتبر است.")
                return render(request, self.template_name, context=context)
            verObj = Verifications.objects.filter(user=user.first(), code=int(code), type=verificationType.email)
            if not verObj.exists():
                context['email'] = True
                messages.warning(request, "کد وارد شده اشتباه است.")
                return render(request, self.template_name, context=context)
            verObj.delete()
            Users.objects.filter(email__iexact=email).update(email_verified_at=timezone.now())
            log(request, logErrCodes.emails, logMessages.emailVerified.format(user.first().username.capitalize(), ),
                user.first().username)
            messages.success(request, "ایمیل شما با موفقیت تایید شد.")
            if 'email' in context:
                del context['email']
            return render(request, self.template_name, context=context)
        return redirect(reverse_lazy("profile"))


class userLogin(View):
    def get(self, request, *args, **kwargs):
        if checkSession(request):
            if not check_active(checkSession(request)):
                messages.error(request, messagesTypes.deAvtive)
                return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
            messages.error(request, messagesTypes.loggedIn)
            return redirect(reverse_lazy('dashboard'))
        return render(request, template_name="login.html", context={})

    def post(self, request):
        if checkSession(request):
            if not check_active(checkSession(request)):
                messages.error(request, messagesTypes.deAvtive)
                return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
            messages.error(request, messagesTypes.loggedIn)
            return redirect(reverse_lazy('dashboard'))

        username = request.POST['user']
        password = request.POST['pass']
        user = Users.objects.filter(username__iexact=username)
        if user.exists():
            if not check_active(user.first().username):
                messages.error(request, messagesTypes.deAvtive)
                return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
            if check_password(password, user.first().password):
                login(request, username)
                log(request, logErrCodes.logInOut, logMessages.loggedIn.format(user.first().username.capitalize(), ),
                    user.first().username)
                messages.success(request, messagesTypes.login.format(user.first().username.capitalize(), ))
                return redirect(reverse_lazy('dashboard'))
            messages.error(request, messagesTypes.invalidUsernameOrPassword)
            return redirect(request.path)
        else:
            messages.error(request, messagesTypes.invalidUsernameOrPassword)
            return redirect(request.path)


class errorsPage(TemplateView, View):
    template_name = "error.html"

    def get(self, request, *args, **kwargs):
        if not checkSession(request):
            messages.error(request, messagesTypes.notlogin)
            return redirect(reverse_lazy("login"))
        if not check_active(checkSession(request)):
            messages.error(request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
        if isinstance(hasAccess("view", "profile", self.request),
                      HttpResponseRedirect) or not Permissions.objects.filter(
            user=Users.objects.filter(username__iexact=checkSession(request)).first()).first().errorsreport:
            messages.error(request, messagesTypes.permissionsNotFound)
            return redirect(reverse_lazy("profile"))
        context = self.get_context_data()
        if request.GET:
            dateFrom = request.GET.get('dateFrom')
            dateTo = request.GET.get('dateTo')
            if dateFrom and dateTo:
                try:
                    convFrom = jdatetime.datetime.strptime(dateFrom.replace("/", "-").replace('از', '').strip(), "%Y-%m-%d").togregorian()
                    convTo = jdatetime.datetime.strptime(dateTo.replace("/", "-").replace('تا','').strip(), "%Y-%m-%d").togregorian()
                except:
                    messages.error(request, "فرمت تاریخ ها اشتباه است.")
                    return redirect(request.path)
                if convTo < convFrom:
                    messages.warning(request, "تاریخ اول نباید بزرگ تر از تاریخ دوم باشد.")
                    return redirect(request.path)
                qs = Faults.objects.filter(created_at__range=(convFrom, convTo))
                if not qs.exists():
                    messages.error(request, f"در بین تاریخ های {dateFrom} و {dateTo} گزارش خطایی پیدا نشد.")
                    return redirect(request.path)
                faults, page_obj = makePagination(qs.order_by('-created_at'), 20, self.request)
                context['pages'] = page_obj
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'گزارش خطا ها'
        faults, page_obj = makePagination(Faults.objects.order_by('-created_at'), 20, self.request)
        context['pages'] = page_obj
        return context


class UserForm(FormView, View):
    template_name = "userprofile.html"
    model = Users
    form_class = userProfileForm
    success_url = reverse_lazy("user")

    @hasAccess("view")
    def get(self, request, *args, **kwargs):
        if not checkSession(request):
            return redirect(reverse_lazy("user"))
        if not check_active(checkSession(request)):
            messages.error(request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(request) else 'login'))
        return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['pageTitle'] = "تنظیمات کاربری"
        data['userform'] = self.form_class
        data['infosform'] = InfosForm()
        data['permform'] = PermissionsForm()
        getUser = getUserinfoByUsername(checkSession(self.request), "groupname")
        if str(getUser).lower() in ["superadmin", "supporter"]:
            data['users'] = Users.objects.exclude(groupname="supporter")
        else:
            data['users'] = Users.objects.exclude(groupname__in=['superadmin', 'supporter'])
        return data

    def form_valid(self, form):
        if not checkSession(self.request):
            messages.error(self.request, messagesTypes.notlogin)
            return redirect(self.success_url)
        if not check_active(checkSession(self.request)):
            messages.error(self.request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(self.request) else 'login'))
        if isinstance(check := hasAccess("view", "settings", self.request), HttpResponseRedirect):
            return check
        field = form.cleaned_data
        username = field.get('username')
        userReq = Users.objects.filter(username__iexact=checkSession(self.request))
        userChecker =  Users.objects.filter(username__iexact=username)
        getUserChecker = userChecker.first().groupname.lower()
        getUserReq = userReq.first().groupname.lower()
        hasAccessOrNot = False
        if not userReq.exists():
            messages.error(self.request, messagesTypes.userInfoNotFound)
            return redirect(reverse_lazy('login'))
        if not userChecker.exists():
            messages.error(self.request, '')
            return redirect(reverse_lazy('user'))
        if getUserReq == 'supporter':
            hasAccessOrNot = getUserChecker in ['superadmin', 'admin', 'user']
        elif getUserReq == 'superadmin':
            hasAccessOrNot = getUserChecker in ['admin', 'user']
        elif getUserReq == 'admin':
            hasAccessOrNot = getUserChecker == 'user'
        elif getUserReq == 'user':
            hasAccessOrNot = False
        if not hasAccessOrNot:
            messages.error(self.request, messagesTypes.permissionsNotFound)
            return redirect(reverse_lazy('user'))

        email = field.get('email')
        extension = field.get('extension')
        fieldReq = self.request.POST
        deleteUser = fieldReq.get('deleteUser')
        saveUser = fieldReq.get('saveUser')
        deleteProfile = fieldReq.get('deleteProfile')
        uploadPhoto = self.request.FILES.get('uploadPhoto')
        ChangePassword = fieldReq.get('ChangePassword')
        nationalcode = fieldReq.get('nationalcode')
        phonenumber = fieldReq.get('phonenumber')
        accountnumbershaba = fieldReq.get('accountnumbershaba')
        cardnumber = fieldReq.get('cardnumber')
        accountnumber = fieldReq.get('accountnumber')
        military = fieldReq.get('military')
        gender = fieldReq.get('gender')
        maritalstatus = fieldReq.get('maritalstatus')
        educationdegree = fieldReq.get('educationdegree')
        province = fieldReq.get('province')
        editOrAdd = field.get('editOrAdd') if field.get('editOrAdd') else fieldReq.get("editOrAdd").lower()
        infosFields = set(InfosForm().fields.keys())
        if username.lower() == checkSession(self.request) and str(getUserinfoByUsername(username, "groupname")) in ['superadmin', 'supporter']:
            infosFields.discard("groupname")
        if fieldReq.get('gender') and fieldReq.get('gender') == "1":
            infosFields = [x for x in infosFields if x != "military"]
        if any(not fieldReq.get(x) for x in infosFields):
            messages.error(self.request, messagesTypes.fillAllFields)
            return redirect(reverse_lazy("user"))
        if editOrAdd == "none":
            messages.error(self.request, messagesTypes.fillAllFields)
            return redirect(reverse_lazy("user"))
        if saveUser:
            if editOrAdd == 'add':
                if isinstance(check := hasAccess("write", "user", self.request), HttpResponseRedirect):
                    return check
                if len(nationalcode) > 10:
                    messages.error(self.request, 'کدملی نامعتبر است.')
                    return redirect(self.success_url)

                if len(phonenumber) != 11:
                    messages.error(self.request, 'شماره همراه نامعتبر است.')
                    return redirect(self.success_url)

                if len(accountnumbershaba) != 22:
                    messages.error(self.request, 'شماره شبا نامعتبر است.')
                    return redirect(self.success_url)

                if len(cardnumber) < 16 and len(cardnumber) > 19:
                    messages.error(self.request, 'شماره کارت نامعتبر است.')
                    return redirect(self.success_url)

                if not gender.isdigit():
                    messages.error(self.request, 'جنسیت نامعتبر است.')
                    return redirect(self.success_url)

                if "groupname" in form.cleaned_data and not form.cleaned_data['groupname'].lower() in ['superadmin', 'admin', 'member'] and not Groups.objects.filter(enname__iexact=form.cleaned_data['groupname']).exists():
                    messages.error(self.request, "نقش نامعتبر است.")
                    return redirect(self.success_url)

                if fieldReq.get('gender') not in ['0', '1', '2']:
                    messages.error(self.request, 'جنسیت نامعتبر است.')
                    return redirect(self.success_url)

                if field.get('gender') == '1':
                    military = None
                else:
                    military = fieldReq.get('military')

                if fieldReq.get('gender') and fieldReq.get('gender') != "1" and fieldReq.get('military') not in ['0',
                                                                                                                 '1',
                                                                                                                 '2',
                                                                                                                 '3',
                                                                                                                 '4']:
                    messages.error(self.request, 'وضعیت سربازی نامعتبر است.')
                    return redirect(self.success_url)

                if not maritalstatus.isdigit():
                    messages.error(self.request, 'وضعیت تاهل نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('maritalstatus') not in ['0', '1']:
                    messages.error(self.request, 'وضعیت تاهل نامعتبر است.')
                    return redirect(self.success_url)

                if not educationdegree.isdigit():
                    messages.error(self.request, 'مدرک تحصیلی نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('educationdegree') not in ['0', '1', '2', '3', '4', '5', '6']:
                    messages.error(self.request, 'مدرک تحصیلی نامعتبر است.')
                    return redirect(self.success_url)

                if not province.isdigit():
                    messages.error(self.request, 'استان نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('province') not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']:
                    messages.error(self.request, 'استان نامعتبر است.')
                    return redirect(self.success_url)

                if Users.objects.filter(username__iexact=username).exists():
                    messages.error(self.request, 'این نام کاربری موجود است.')
                    return redirect(self.success_url)

                if Users.objects.filter(email__iexact=email).exists():
                    messages.error(self.request, 'این ایمیل موجود است.')
                    return redirect(self.success_url)

                if Users.objects.filter(extension=extension).exists():
                    messages.error(self.request, 'این داخلی موجود است.')
                    return redirect(self.success_url)

                if Users.objects.filter(extension=int(extension)).exists():
                    messages.error(self.request, 'این داخلی موجود است.')
                    return redirect(self.success_url)

                if not nationalcode.isdigit():
                    messages.error(self.request, 'این کدملی موجود است.')
                    return redirect(self.success_url)

                if Infos.objects.filter(nationalcode=int(nationalcode)).exists():
                    messages.error(self.request, 'این کدملی موجود است.')
                    return redirect(self.success_url)

                if not phonenumber.isdigit():
                    messages.error(self.request, 'این شماره همراه موجود است.')
                    return redirect(self.success_url)

                if Infos.objects.filter(phonenumber=int(phonenumber)).exists():
                    messages.error(self.request, 'این شماره همراه موجود است.')
                    return redirect(self.success_url)

                if Infos.objects.filter(accountnumbershaba=accountnumbershaba).exists():
                    messages.error(self.request, 'این شماره شبا موجود است.')
                    return redirect(self.success_url)

                if not cardnumber.isdigit():
                    messages.error(self.request, 'این شماره کارت موجود است.')
                    return redirect(self.success_url)

                if Infos.objects.filter(cardnumber=int(cardnumber)).exists():
                    messages.error(self.request, 'این شماره کارت موجود است.')
                    return redirect(self.success_url)

                if not accountnumber.isdigit():
                    messages.error(self.request, 'این شماره حساب موجود است.')
                    return redirect(self.success_url)

                if Infos.objects.filter(accountnumber=int(accountnumber)).exists():
                    messages.error(self.request, 'این شماره حساب موجود است.')
                    return redirect(self.success_url)

                if uploadPhoto:

                    valid = validatePhotoExt(uploadPhoto.name)
                    if not valid:
                        messages.error(self.request, 'پسوند فایل ارسال شده نامعتبر میباشد.')
                        return redirect(self.success_url)
                    filename = f"{username.lower()}_photo{valid.lower()}"
                    filepath = os.path.join('Alvand/static/upload', filename)

                    with open(filepath, '+wb') as f:
                        for bt in uploadPhoto:
                            f.write(bt)
                    picurl = filename
                else:
                    picurl = 'avatar.png'
                user = form.save(commit=False)

                user.group = Groups.objects.filter(enname=form.cleaned_data['groupname']).first()
                user.groupname = form.cleaned_data['groupname'].lower()
                if picurl:
                    user.picurl = picurl
                listOfExts = fieldReq.getlist('usersextension')
                labels = []
                nonLabels = []
                if any(l for l in listOfExts):
                    for item in listOfExts:
                        item = item.strip()
                        if Extensionsgroups.objects.filter(label=str(item)).exists():
                            labels.append(item)
                        elif item.isdigit() and (
                                Users.objects.filter(extension=int(item)).exists() or Records.objects.filter(
                            extension=str(item)).exists()):
                            nonLabels.append(str(item))
                if nonLabels:
                    user.usersextension = nonLabels
                user.password = make_password("123456789")
                user.save()
                if labels:
                    Permissions.objects.create(user=user, can_view=bool(fieldReq.get("can_view")),
                                               can_write=bool(fieldReq.get("can_write")),
                                               can_modify=bool(fieldReq.get("can_modify")),
                                               can_delete=bool(fieldReq.get("can_delete")), exts_label=labels)
                else:
                    Permissions.objects.create(user=user, can_view=bool(fieldReq.get("can_view")),
                                               can_write=bool(fieldReq.get("can_write")),
                                               can_modify=bool(fieldReq.get("can_modify")),
                                               can_delete=bool(fieldReq.get("can_delete")))
                Infos.objects.create(user=user, gender=gender, nationalcode=nationalcode,
                                     birthdate=fieldReq.get('birthdate'),
                                     telephone=fieldReq.get('telephone'), phonenumber=phonenumber,
                                     maritalstatus=maritalstatus,
                                     military=military, educationfield=fieldReq.get('educationfield'),
                                     educationdegree=educationdegree,
                                     province=province, city=fieldReq.get('city'),
                                     accountnumbershaba=accountnumbershaba,
                                     cardnumber=cardnumber, accountnumber=accountnumber,
                                     address=fieldReq.get('address'))

                messages.success(self.request, f'کاربر {username} با موفقیت به جمع ما پیوست.')
            elif editOrAdd == 'edit':
                if isinstance(check := hasAccess("modify", "user", self.request), HttpResponseRedirect):
                    return check
                user = Users.objects.filter(username__iexact=username).first()
                if not user:
                    messages.error(self.request, 'کاربر مورد نظر موجود نیست.')
                    return redirect(reverse_lazy("user"))

                userInfo = Infos.objects.filter(user=user).first()
                if user.email.lower() != email.lower():
                    if Users.objects.filter(email__iexact=email).exists():
                        messages.error(self.request, 'این ایمیل موجود است.')
                        return redirect(self.success_url)

                if user.extension != int(extension):
                    if Users.objects.filter(extension=int(extension)).exists():
                        messages.error(self.request, 'این داخلی موجود است.')
                        return redirect(self.success_url)

                if not nationalcode.isdigit():
                    messages.error(self.request, 'لطفا کد ملی را به صورت اعداد بنویسید.')
                    return redirect(self.success_url)

                if userInfo.nationalcode != int(nationalcode):
                    if Infos.objects.filter(nationalcode=int(nationalcode)).exists():
                        messages.error(self.request, 'این کدملی موجود است.')
                        return redirect(self.success_url)

                if "groupname" in form.cleaned_data and not form.cleaned_data['groupname'].lower() in ['superadmin', 'admin', 'member'] and not Groups.objects.filter(enname__iexact=form.cleaned_data['groupname']).exists():
                    messages.error(self.request, "نقش نامعتبر است.")
                    return redirect(self.success_url)

                if not phonenumber.isdigit():
                    messages.error(self.request, 'لطفا شماره همراه را به صورت اعداد بنویسید.')
                    return redirect(self.success_url)
                if int(userInfo.phonenumber) != int(phonenumber):
                    if Infos.objects.filter(phonenumber=int(phonenumber)).exists():
                        messages.error(self.request, 'این شماره همراه موجود است.')
                        return redirect(self.success_url)

                if str(userInfo.accountnumbershaba) != str(accountnumbershaba):
                    if Infos.objects.filter(accountnumbershaba=accountnumbershaba).exists():
                        messages.error(self.request, 'این شماره شبا موجود است.')
                        return redirect(self.success_url)

                if not cardnumber.isdigit():
                    messages.error(self.request, 'لطفا شماره کارت را به صورت اعداد بنویسید.')
                    return redirect(self.success_url)

                if str(userInfo.cardnumber) != str(cardnumber):
                    if Infos.objects.filter(cardnumber=cardnumber).exists():
                        messages.error(self.request, 'این شماره کارت موجود است.')
                        return redirect(self.success_url)

                if not accountnumber.isdigit():
                    messages.error(self.request, 'لطفا شماره حساب را به صورت اعداد بنویسید.')
                    return redirect(self.success_url)

                if int(userInfo.accountnumber) != int(accountnumber):
                    if Infos.objects.filter(accountnumber=accountnumber).exists():
                        messages.error(self.request, 'این شماره حساب موجود است.')
                        return redirect(self.success_url)

                if len(nationalcode) > 10:
                    messages.error(self.request, 'کدملی نامعتبر است.')
                    return redirect(self.success_url)

                if len(phonenumber) > 11:
                    messages.error(self.request, 'شماره همراه نامعتبر است.')
                    return redirect(self.success_url)

                if len(accountnumbershaba) != 22:
                    messages.error(self.request, 'شماره شبا نامعتبر است.')
                    return redirect(self.success_url)

                if len(cardnumber) < 16 and len(cardnumber) > 19:
                    messages.error(self.request, 'شماره کارت نامعتبر است.')
                    return redirect(self.success_url)

                if not gender.isdigit():
                    messages.error(self.request, 'جنسیت نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('gender') not in ['0', '1', '2']:
                    messages.error(self.request, 'جنسیت نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('gender') and fieldReq.get('gender') != "1" and fieldReq.get('military') not in ['0',
                                                                                                                 '1',
                                                                                                                 '2',
                                                                                                                 '3',
                                                                                                                 '4']:
                    messages.error(self.request, 'وضعیت سربازی نامعتبر است.')
                    return redirect(self.success_url)

                if field.get('gender') == '1':
                    military = None
                else:
                    military = fieldReq.get('military')

                if not maritalstatus.isdigit():
                    messages.error(self.request, 'وضعیت تاهل نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('maritalstatus') not in ['0', '1']:
                    messages.error(self.request, 'وضعیت تاهل نامعتبر است.')
                    return redirect(self.success_url)

                if not educationdegree.isdigit():
                    messages.error(self.request, 'مدرک تحصیلی نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('educationdegree') not in ['0', '1', '2', '3', '4', '5', '6']:
                    messages.error(self.request, 'مدرک تحصیلی نامعتبر است.')
                    return redirect(self.success_url)

                if not province.isdigit():
                    messages.error(self.request, 'استان نامعتبر است.')
                    return redirect(self.success_url)

                if fieldReq.get('province') not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']:
                    messages.error(self.request, 'استان نامعتبر است.')
                    return redirect(self.success_url)
                listOfExts = fieldReq.getlist('usersextension')
                labels = []
                nonLabels = []
                if any(l for l in listOfExts):
                    for item in listOfExts:
                        item = item.strip()
                        if Extensionsgroups.objects.filter(label=str(item)).exists():
                            labels.append(item)
                        elif item.isdigit() and (
                                Users.objects.filter(extension=int(item)).exists() or Records.objects.filter(
                            extension=str(item)).exists()):
                            nonLabels.append(str(item))
                filename = "avatar.png"
                if uploadPhoto:
                    valid = validatePhotoExt(uploadPhoto.name)
                    if not valid:
                        messages.error(self.request, 'پسوند فایل ارسال شده نامعتبر میباشد.')
                        return redirect(self.success_url)
                    filename = f"{username.lower()}_photo{valid.lower()}"
                    filepath = os.path.join('Alvand/static/upload', filename)

                    with open(filepath, '+wb') as f:
                        for bt in uploadPhoto:
                            f.write(bt)
                checkuserobj = Users.objects.filter(username__iexact=username)
                gp = Groups.objects.filter(enname__iexact=form.cleaned_data['groupname']).first() if "groupname" in form.cleaned_data else None
                if uploadPhoto:
                    if checkuserobj.exists():
                        if username.lower() == checkSession(self.request) and str(getUserinfoByUsername(username, "groupname")) in ['superadmin', 'supporter']:
                            checkuserobj.update(name=field.get('name'),
                                                lastname=field.get('lastname'), extension=extension,
                                                email=email, usersextension=nonLabels, active=bool(field.get('active')),
                                                picurl=filename)
                        else:
                            checkuserobj.update(name=field.get('name'),
                                                lastname=field.get('lastname'), extension=extension,
                                                email=email, usersextension=nonLabels, active=bool(field.get('active')),
                                                picurl=filename, group=gp, groupname=form.cleaned_data['groupname'].lower())
                else:
                    if checkuserobj.exists():
                        if username.lower() == checkSession(self.request) and str(getUserinfoByUsername(username, "groupname")) in ['superadmin', 'supporter']:
                            checkuserobj.update(name=field.get('name'),
                                              lastname=field.get('lastname'), extension=extension,
                                               email=email, usersextension=nonLabels, active=bool(field.get('active')))
                        else:
                            checkuserobj.update(name=field.get('name'),
                                                lastname=field.get('lastname'), extension=extension,
                                                email=email, usersextension=nonLabels, active=bool(field.get('active')),
                                                group=gp, groupname=form.cleaned_data['groupname'].lower())
                if checkuserobj.exists():
                    perm = Permissions.objects.filter(user=checkuserobj.first())
                    if perm.exists():
                        perm.update(can_view=bool(fieldReq.get("can_view")), can_write=bool(fieldReq.get("can_write")),
                                    can_modify=bool(fieldReq.get("can_modify")),
                                    can_delete=bool(fieldReq.get("can_delete")), exts_label=labels)
                    inf = Infos.objects.filter(user=checkuserobj.first())
                    if inf.exists():
                        inf.update(gender=gender, nationalcode=nationalcode,
                                   birthdate=fieldReq.get('birthdate'),
                                   telephone=fieldReq.get('telephone'),
                                   phonenumber=phonenumber,
                                   maritalstatus=maritalstatus,
                                   military=military,
                                   educationfield=fieldReq.get(
                                       'educationfield'),
                                   educationdegree=educationdegree,
                                   province=province, city=fieldReq.get('city'),
                                   accountnumbershaba=accountnumbershaba,
                                   cardnumber=cardnumber,
                                   accountnumber=accountnumber,
                                   address=fieldReq.get('address'))

                messages.success(self.request, f'اطلاعات کاربر {username} با موفقیت بروز شد.')

            else:
                messages.error(self.request,
                               'برای انجام عملیات ویرایش یا اضافه کاربر باید گزینه مناسب را در فیلد ویرایش/اضافه انتخاب کنید.')
                return redirect(reverse_lazy("user"))
        elif deleteUser:
            if isinstance(check := hasAccess("delete", "user", self.request), HttpResponseRedirect):
                return check
            if editOrAdd == 'edit':
                username = form.cleaned_data.get('username')
                found_user = Users.objects.filter(username__iexact=username)
                if found_user.exists():
                    if username.lower() == checkSession(self.request) and str(getUserinfoByUsername(username, "groupname")) in ['superadmin', 'supporter']:
                        messages.error(self.request, "شما نمی توانید حساب کاربری بالاترین مقام را حذف کنید.")
                        return redirect(self.success_url)
                    Extensionsgroups.objects.filter(modifyby=found_user.first()).delete()
                    Infos.objects.filter(user=found_user.first()).delete()
                    Permissions.objects.filter(user=found_user.first()).delete()
                    Verifications.objects.filter(user=found_user.first()).delete()
                    filename = found_user.first().picurl
                    if filename in os.listdir('Alvand/static/upload'):
                        os.remove(f'Alvand/static/upload/{filename}')
                    found_user.delete()
                    messages.success(self.request, f'کاربر {username} با موفقیت حذف شد')
                    return redirect(self.success_url)
                else:
                    messages.error(self.request, f'کاربر {username} وجود ندارد')
                    return redirect(self.success_url)

            messages.error(self.request, 'برای حذف کاربر باید مقدار ویرایش را انتخاب کنید.')
        elif deleteProfile:
            if isinstance(check := hasAccess("delete", "user", self.request), HttpResponseRedirect):
                return check
            if editOrAdd == 'edit':
                username = form.cleaned_data.get('username')
                found_user_pro = Users.objects.filter(username__iexact=username)
                if found_user_pro.exists():
                    if found_user_pro.first().picurl.lower() == "avatar.png":
                        messages.error(self.request, f'کاربر {username} عکسی ندارد.')
                        return redirect(self.success_url)
                    else:
                        filename = found_user_pro.first().picurl
                        if filename in os.listdir('Alvand/static/upload'):
                            os.remove(f'Alvand/static/upload/{filename}')

                        found_user_pro.update(picurl='avatar.png')
                        messages.success(self.request, f'پروفایل کاربر {username} با موفقیت حذف شد.')
                        return redirect(self.success_url)
                else:
                    messages.error(self.request, f' کاربر {username} وجود ندارد.')
                    return redirect(self.success_url)
            else:
                messages.error(self.request, 'برای حذف پروفایل کاربر باید مقدار ویرایش را انتخاب کنید.')
                return redirect(self.success_url)
        elif ChangePassword:
            if editOrAdd == 'edit':
                username = form.cleaned_data.get('username')
                found_user = Users.objects.filter(username__iexact=username)
                if found_user.exists():
                    psw = 123456789
                    if check_password(psw, found_user.first().password):
                        messages.error(self.request, f'رمز عبور کاربر {username} قبلا بازنگاری شده است.')
                        return redirect(self.success_url)
                    Users.objects.update(password=make_password('123456789'))
                    messages.success(self.request, f'رمز عبور کاربر {username} با موفقیت بازنگاری شد.')
                    return redirect(self.success_url)
                else:
                    messages.error(self.request, f'کاربر {username} وجود ندارد.')
                    return redirect(self.success_url)

            messages.error(self.request, 'برای حذف پروفایل کاربر باید مقدار ویرایش را انتخاب کنید.')
            return redirect(self.success_url)
        else:
            if isinstance(check := hasAccess("view", "user", self.request), HttpResponseRedirect):
                return check
            messages.error(self.request, "درخواست ارسال شده نامعتبر است.")

        return super().form_valid(form)

    def form_invalid(self, form):
        if not checkSession(self.request):
            messages.error(self.request, messagesTypes.notlogin)
            return redirect(self.success_url)
        if not check_active(checkSession(self.request)):
            messages.error(self.request, messagesTypes.deAvtive)
            return redirect(reverse_lazy('logout' if checkSession(self.request) else 'login'))
        if isinstance(check := hasAccess("view", "settings", self.request), HttpResponseRedirect):
            return check
        if self.request.POST.get('deleteUser'):
            return self.form_valid(form)
        if self.request.POST.get('deleteProfile'):
            return self.form_valid(form)
        if self.request.POST.get(form):
            return self.form_valid('ChangePassword')
        if self.request.POST.get('saveUser') and str(self.request.POST.get('username')) == checkSession(self.request) and str(getUserinfoByUsername(checkSession(self.request), "groupname")) in ['superadmin', 'supporter']:
            return self.form_valid(form)
        messages.error(self.request, messagesTypes.fillAllFields)
        return redirect(reverse_lazy("user"))


def index(request):
    return redirect(reverse_lazy("dashboard"))

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        # Handle QuerySets and other Django-specific objects if needed
        if isinstance(obj, models.QuerySet):
            return list(obj.values())
        return super().default(obj)

def userprofile_view(request):
    users_queryset = Users.objects.all()
    session_user_obj = request.session.get('user', None)

    users_data = []
    for user in users_queryset:
        user_dict = {
            'username': user.username,
            'name': user.name,
            'lastname': user.lastname,
            'extension': user.extension,
            'email': user.email,
            'active': user.active,
            'groupname': user.groupname,
            'picurl': user.picurl if user.picurl else 'avatar.png',
            'usersextension': list(user.usersextension.values_list('field_name', flat=True)),
            'getListOfExtsGroups': getListOfExtsGroups(user.username),
            'getUserCanPerm': getUserCanPerm(user.username),
            'getObjectOfInfo': list(getObjectOfInfo(user.username).values())
        }
        users_data.append(user_dict)
    
    session_user_data = {}
    if session_user_obj:
        session_user_data = {
            'username': session_user_obj.username,
            'getUserInfo_groupname': getUserInfo(session_user_obj, "groupname")
        }

    all_contact_infos = []
    for user_obj in users_queryset:
        infos = getObjectOfInfo(user_obj.username)
        for info in infos:
            info_dict = {
                'username': user_obj.username,
                'nationalcode': info.nationalcode,
                'birthdate': str(info.birthdate) if info.birthdate else None,
                'telephone': info.telephone,
                'phonenumber': info.phonenumber,
                'gender': info.gender,
                'maritalstatus': info.maritalstatus,
                'military': info.military,
                'educationfield': info.educationfield,
                'educationdegree': info.educationdegree,
                'province': info.province,
                'city': info.city,
                'accountnumbershaba': info.accountnumbershaba,
                'cardnumber': info.cardnumber,
                'accountnumber': info.accountnumber,
                'address': info.address,
            }
            all_contact_infos.append(info_dict)

    context = {
        'users': json.dumps(users_data, cls=CustomJSONEncoder),
        'session_user': json.dumps(session_user_data, cls=CustomJSONEncoder),
        'contactInfos': json.dumps(all_contact_infos, cls=CustomJSONEncoder),
    }
    
    return render(request, 'Alvand/templates/userprofile.html', context)
