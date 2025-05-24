from django.template import Library
from Alvand.models import Users, lices, VERSIONS
from Alvand.views import getTupleIndex

register = Library()

@register.filter
def getBaseInfo(username, value):
    if not username: return None
    qs = Users.objects.filter(username__iexact=username)
    if not qs.exists():
        return None
    return next(iter(qs.values(value).first().values()))

@register.filter
def getVersion():
    version = lices.objects.all()
    if not version.exists():
        return None
    return getTupleIndex(VERSIONS, version.first().version)