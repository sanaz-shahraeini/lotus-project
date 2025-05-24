from django.template import Library
from Alvand.models import Errors
import jdatetime, datetime

register = Library()

@register.filter
def getDataOfFields(code, field):
    if not isinstance(code, int): return None
    qs = Errors.objects.filter(errorcodenum=int(code))
    if not qs.exists():
        return None
    if not field in qs.values().first(): return None
    return next(iter(qs.values(field).first().values()))

@register.filter
def convertDatesToHijri(date):
    try:
        y, m, d = map(int, date.replace("-", "/").split("/"))
        return jdatetime.datetime.fromgregorian(year=y, month=m, day=d).strftime("%Y/%m/%d")
    except:
        return date