from django.template import Library
from Alvand.models import Users, Infos, Groups, GENDER, MILITARY, MARITALSTATUS, DEGREE, PROVINCE
from Alvand.views import getTupleIndex


register = Library()

@register.filter
def getFieldOfInfo(username, field):
    if not isinstance(username, str): return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return None
    qs = Infos.objects.filter(user=user.first())
    if not qs.exists(): return None
    if not field in qs.values().first(): return None
    return next(iter(qs.values(field).first().values()))

@register.filter
def getGroupnameById(_id):
    if not _id: return None
    try:
        qs = Groups.objects.filter(id=_id.id)
        if not qs.exists():
            return None
        return next(iter(qs.values('pename').first().values()))
    except:
        return None

@register.filter
def getValueOfIndexes(index, name):
    if not name or not str(index): return None
    if not name.lower() in ['gender', 'military', 'marital', 'degree', 'province']: return None
    name = name.lower()
    if name == "gender":
        result = getTupleIndex(GENDER, str(index))
    elif name == "military":
        result = getTupleIndex(MILITARY, str(index))
    elif name == "marital":
        result = getTupleIndex(MARITALSTATUS, str(index))
    elif name == "degree":
        result = getTupleIndex(DEGREE, str(index))
    elif name == "province":
        result = getTupleIndex(PROVINCE, str(index))
    else: result = None
    return result