from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

"""
    NOTE: Fields such as created_at or similar fields use the default=timezone.now parameter. This 
    parameter, when used with the jdatetime library, is for Persian (Jalali) date and time representation. It replaces 
    the default datetime (Gregorian) library for date and time handling in the next version of this web application.
"""

GENDER = (
    ('0', 'مرد'),
    ('1', 'زن'),
    ('2', 'نامعلوم')
)

MILITARY = (
    ('0', 'مشمول'),
    ('1', 'پایان خدمت'),
    ('2', 'معافیت پزشکی'),
    ('3', 'معافیت تحصیلی'),
    ('4', 'معافیت سایر')

)

MARITALSTATUS = (
    ('0', 'متاهل'),
    ('1', 'مجرد')

)

DEGREE = (
    ('0', 'زیر دیپلم'),
    ('1', 'دیپلم'),
    ('2', 'فوق دیپلم'),
    ('3', 'لیسانس '),
    ('4', 'فوق لیسانس'),
    ('5', 'دکترا'),
    ('6', 'فوق دکترا')

)

PROVINCE = (
    ('0', 'آذربایجان شرقی'),
    ('1', 'آذربایجان غربی'),
    ('2', '	اردبیل'),
    ('3', 'اصفهان'),
    ('4', 'البرز'),
    ('5', 'ایلام'),
    ('6', 'بوشهر'),
    ('7', '	تهران'),
    ('8', 'چهارمحال و بختیاری'),
    ('9', 'خراسان جنوبی'),
    ('10', 'خراسان رضوی'),
    ('11', 'خراسان شمالی'),
    ('12', 'خوزستان'),
    ('13', 'زنجان'),
    ('14', 'سمنان'),
    ('15', 'سیستان و بلوچستان'),
    ('16', 'فارس'),
    ('17', 'قزوین'),
    ('18', 'قم'),
    ('19', 'کردستان'),
    ('20', 'کرمان'),
    ('21', 'کرمانشاه'),
    ('22', 'کهگیلویه و بویراحمد'),
    ('23', 'گلستان'),
    ('24', 'گیلان'),
    ('25', 'لرستان'),
    ('26', 'مازندران'),
    ('27', 'مرکزی'),
    ('28', 'هرمزگان'),
    ('29', 'همدان'),
    ('30', 'یزد')
)
DEVICE = (
    ('KX-TA308', 'KX-TA308'),
    ('KX-TES824', 'KX-TES824'),
    ('KX-TEM824', 'KX-TEM824'),
    ('KX-TDA30', 'KX-TDA30'),
    ('KX-TDA100', 'KX-TDA100'),
    ('KX-TDA100D', 'KX-TDA100D'),
    ('KX-TDA100DBA', 'KX-TDA100DBA'),
    ('KX-TDA200', 'KX-TDA200'),
    ('KX-TDA600', 'KX-TDA600'),
    ('KX-TDE100', 'KX-TDE100'),
    ('KX-TDE200', 'KX-TDE200'),
    ('KX-TDE600', 'KX-TDE600'),
    ('KX-NS300', 'KX-NS300'),
    ('KX-NS500', 'KX-NS500'),
    ('KX-NS700', 'KX-NS700'),
    ('KX-NS1000', 'KX-NS1000'),
    ('KX-HTS32', 'KX-HTS32'),
    ('KX-HTS824', 'KX-HTS824'),
)
BUADRATE = (
    (4800, '4800'),
    (9600, '9600'),
    (19200, '19200'),
    (38400, '38400'),
    (57600, '57600'),
    (112500, '112500'),
    (230400, '230400'),
    (460800, '460800'),
    (921600, '921600')
)
PARITY = (
    ('None', 'None'),
    ('Odd', 'Odd'),
    ('Even', 'Even'),
    ('Mark', 'Mark'),
    ('Space', 'Space')
)
DATABITS = (
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8')
)
STOPBITS = (
    (1, '1'),
    (1.5, '1.5'),
    (2, '2')
)
FLOW = (
    ('None', 'None'),
    ('XON/XOFF', 'XON/XOFF'),
    ('RTS/CTS', 'RTS/CTS'),
    ('DSR/DTR', 'DSR/DTR')
)

LINES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10')
)

VERSIONS = (
    ('alvand', 'الوند'),
    ('binalud', 'بینالود')
)

CABLE_TYPES = (
    ('rs-232c', 'RS-232C'),
    ('ethernet', 'ETHERNET'),
)

class ArrayAppend(models.Func):
    function = "array_append"
    arity = 2


class Connections(models.Model):
    state = models.CharField(max_length=11)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


# TODO: THIS IS CONTACT APPLICATION LIKE CONTACT APPLICATION IN PHONES, IN NEXT VERSION WILL BE ADDED
# class Contacts(models.Model):
#     user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user')
#     gender = models.CharField(max_length=191, blank=True, null=True)
#     birthdate = models.CharField(max_length=10, blank=True, null=True)
#     mobile = ArrayField(models.CharField(), blank=True, null=True)
#     landline = ArrayField(models.CharField(), blank=True, null=True)
#     educationfield = models.CharField(max_length=191, blank=True, null=True)
#     educationdegree = models.CharField(max_length=191, blank=True, null=True)
#     militarystate = models.CharField(max_length=191, blank=True, null=True)
#     maritalstatus = models.CharField(max_length=191, blank=True, null=True)
#     website = models.CharField(max_length=191, blank=True, null=True)
#     email = models.CharField(max_length=191, blank=True, null=True)
#     instagram = models.CharField(max_length=191, blank=True, null=True)
#     telegram = models.CharField(max_length=191, blank=True, null=True)
#     whatsapp = models.CharField(max_length=191, blank=True, null=True)
#     facebook = models.CharField(max_length=191, blank=True, null=True)
#     twitter = models.CharField(max_length=191, blank=True, null=True)
#     companyname = models.CharField(max_length=191, blank=True, null=True)
#     jobtitle = models.CharField(max_length=191, blank=True, null=True)
#     workphone = models.CharField(max_length=191, blank=True, null=True)
#     internal = models.CharField(max_length=191, blank=True, null=True)
#     directphone = models.CharField(max_length=191, blank=True, null=True)
#     relationship = models.CharField(max_length=191, blank=True, null=True)
#     country = models.CharField(max_length=191, blank=True, null=True)
#     province = models.CharField(max_length=191, blank=True, null=True)
#     city = models.CharField(max_length=191, blank=True, null=True)
#     address = models.CharField(max_length=191, blank=True, null=True)
#     notes = models.CharField(max_length=500, blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)


class Costs(models.Model):
    hamrahaval = models.FloatField()
    irancell = models.FloatField()
    rightel = models.FloatField()
    provincial = models.FloatField()
    international = models.FloatField()
    outofprovincial = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Countries(models.Model):
    summary = models.CharField(unique=True, max_length=4)
    title = models.CharField(unique=True, max_length=25)


class Device(models.Model):
    device = models.CharField(choices=DEVICE, max_length=191)
    stopbits = models.FloatField(choices=STOPBITS, blank=True, null=True)
    baudrate = models.BigIntegerField(choices=BUADRATE, blank=True, null=True)
    parity = models.TextField(choices=PARITY, blank=True, null=True)
    databits = models.IntegerField(choices=DATABITS, blank=True, null=True)
    flow = models.TextField(choices=FLOW, blank=True, null=True)
    number_of_lines = models.BigIntegerField(blank=True, null=True)
    smdrip = models.TextField(blank=True, null=True)
    smdrport = models.IntegerField(blank=True, null=True)
    smdrpassword = models.TextField(blank=True, null=True)
    cable_type = models.CharField(blank=True, null=True, choices=CABLE_TYPES)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Emailsending(models.Model):
    emailtosend = models.EmailField()
    collectionusername = models.TextField()
    collectionpassword = models.TextField()
    lines = models.IntegerField(default=1, choices=LINES)
    errors = ArrayField(models.BigIntegerField(), blank=True, null=True)
    byadmin = models.ForeignKey('Users', models.CASCADE, db_column="byadmin")
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Errors(models.Model):
    errorcodenum = models.BigIntegerField(unique=True)
    errormessage = models.TextField(blank=True, null=True)
    probablecause = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Extensionsgroups(models.Model):
    exts = ArrayField(models.BigIntegerField(), blank=True, null=True)
    label = models.TextField()
    modifyby = models.ForeignKey('Users', models.DO_NOTHING, db_column='modifyby')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class Faults(models.Model):
    date_time = models.DateTimeField(blank=True, null=True)
    errorcode = models.BigIntegerField()
    label = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Groups(models.Model):
    active = models.BooleanField(blank=True, null=True)
    pename = models.CharField(max_length=200)
    enname = models.CharField(max_length=200)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (('pename', 'enname'),)


class Infos(models.Model):
    user = models.ForeignKey('Users', models.CASCADE, db_column='user')
    birthdate = models.TextField(blank=True, null=True, verbose_name='تاریخ تولد:')
    phonenumber = models.CharField(max_length=191, blank=True, null=True, verbose_name='شماره همراه:')
    telephone = models.CharField(max_length=191, blank=True, null=True, verbose_name='تلفن:')
    province = models.CharField(choices=PROVINCE, max_length=191, blank=True, null=True, verbose_name='استان:')
    city = models.CharField(max_length=191, blank=True, null=True, verbose_name='شهر:')
    address = models.CharField(max_length=191, blank=True, null=True, verbose_name='آدرس:')
    gender = models.IntegerField(choices=GENDER, blank=True, null=True, verbose_name='جنسیت:')
    military = models.CharField(choices=MILITARY, max_length=191, blank=True, null=True,
                                verbose_name='وضعیت نظام وظیفه:')
    maritalstatus = models.CharField(choices=MARITALSTATUS, max_length=191, blank=True, null=True,
                                     verbose_name='وضعیت تاهل:')
    educationdegree = models.CharField(choices=DEGREE, max_length=191, blank=True, null=True, verbose_name='مدرک:')
    educationfield = models.CharField(max_length=191, blank=True, null=True, verbose_name='زمینه مدرک:')
    cardnumber = models.CharField(max_length=191, blank=True, null=True, verbose_name='شماره کارت:')
    accountnumber = models.CharField(max_length=191, blank=True, null=True, verbose_name='شماره حساب:')
    accountnumbershaba = models.CharField(max_length=191, blank=True, null=True, verbose_name='شماره حساب:')
    macaddress = models.CharField(max_length=191, blank=True, null=True, default=None, verbose_name='مک آدرس:')
    nationalcode = models.BigIntegerField(blank=True, null=True, verbose_name='کد ملی:')
    groupname = models.CharField(max_length=191, blank=True, null=True, verbose_name='نقش:')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class Permissions(models.Model):
    user = models.ForeignKey('Users', models.CASCADE, db_column='user')
    perm_email = models.BooleanField(blank=True, null=True)
    can_view = models.BooleanField(default=False, verbose_name="مجوز دیدن")
    can_write = models.BooleanField(default=False, verbose_name="مجوز ایجاد کردن")
    can_delete = models.BooleanField(default=False, verbose_name="مجوز حذف کردن")
    can_modify = models.BooleanField(default=False, verbose_name="مجوز ویرایش کردن")
    exts_label = ArrayField(models.CharField(), blank=True, null=True)
    errorsreport = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class Records(models.Model):
    date = models.DateField(verbose_name="تاریخ:")
    hour = models.TimeField(verbose_name="ساعت:")
    extension = models.CharField(max_length=200, blank=True, null=True)
    urbanline = models.CharField(max_length=200, blank=True, null=True)
    contactnumber = models.CharField(max_length=200, blank=True, null=True)
    calltype = models.CharField(max_length=200)
    durationtime = models.CharField(max_length=200, blank=True, null=True)
    internal = models.BigIntegerField(blank=True, null=True)
    beepsnumber = models.CharField(max_length=200, blank=True, null=True)
    transferring = ArrayField(models.CharField(), blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class Telephons(models.Model):
    type = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=200)
    code = models.CharField(unique=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Users(models.Model):
    active = models.BooleanField(default=True)
    online = models.IntegerField(default=True)
    extension = models.BigIntegerField()
    usersextension = ArrayField(models.CharField(), verbose_name="دسترسی های داخلی:", blank=True, null=True)
    name = models.CharField(max_length=191, verbose_name="نام:")
    username = models.CharField(max_length=191, verbose_name="نام کاربری:")
    lastname = models.CharField(max_length=191, verbose_name="نام خانوادگی:")
    group = models.ForeignKey(Groups, models.DO_NOTHING)
    groupname = models.CharField(max_length=191)
    picurl = models.CharField(max_length=191, default="avatar.png")
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=191)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=191)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class Verifications(models.Model):
    user = models.ForeignKey(Users, models.CASCADE, db_column='user')
    type = models.IntegerField(default=0)
    code = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)


class Log(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column="user")
    userBackup = models.CharField(max_length=200)
    errCode = models.CharField(max_length=100)
    errMessage = models.TextField()
    macAddress = models.TextField(default=None, blank=True, null=True, max_length=250)
    ip = models.GenericIPAddressField()
    byWho = models.CharField(max_length=100, default="Lotus")
    created_at = models.DateTimeField(auto_now_add=True)


class ContactInfo(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    province = models.CharField(choices=PROVINCE, max_length=191, verbose_name='استان:')
    phone_number = models.CharField(max_length=191, verbose_name='شماره همراه مدیر:')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class errorsSent(models.Model):
    fault = models.ForeignKey(Faults, models.CASCADE)
    success = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class lices(models.Model):
    lice = models.TextField(max_length=500, default=None)
    active = models.BooleanField(default=False)
    version = models.CharField(max_length=50, choices=VERSIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class SMDRRecord(models.Model):
    date = models.DateField(verbose_name="تاریخ")
    time = models.TimeField(verbose_name="زمان")
    ext = models.CharField(max_length=50, verbose_name="داخلی", blank=True, null=True)
    co = models.CharField(max_length=50, verbose_name="خط شهری", blank=True, null=True)
    dial_number = models.CharField(max_length=200, verbose_name="شماره گرفته شده", blank=True, null=True)
    ring_time = models.CharField(max_length=50, verbose_name="زمان زنگ", blank=True, null=True)
    duration = models.CharField(max_length=50, verbose_name="مدت تماس", blank=True, null=True)
    acc_code = models.CharField(max_length=50, verbose_name="کد دسترسی", blank=True, null=True)
    cd_code = models.CharField(max_length=50, verbose_name="کد CD", blank=True, null=True)
    call_type = models.CharField(max_length=50, verbose_name="نوع تماس", blank=True, null=True)
    is_internal = models.BooleanField(default=False, verbose_name="تماس داخلی")
    is_incoming = models.BooleanField(default=False, verbose_name="تماس ورودی")
    is_outgoing = models.BooleanField(default=False, verbose_name="تماس خروجی")
    is_system_message = models.BooleanField(default=False, verbose_name="پیام سیستمی")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date} {self.time} - {self.ext} - {self.dial_number}"
    
    class Meta:
        verbose_name = "گزارش SMDR"
        verbose_name_plural = "گزارش های SMDR"
        ordering = ['-date', '-time']
