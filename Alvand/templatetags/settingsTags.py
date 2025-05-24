from django.template import Library
from Alvand.models import Extensionsgroups, Users, Permissions
import json

register = Library()

@register.filter
def getExtsFromExtGroups(label):
    if not isinstance(label, str): return []
    extgps = Extensionsgroups.objects.filter(label__iexact=label)
    if not extgps.exists():
        return []
    return extgps.first().exts

@register.filter
def getExtReportPerm(username):
    if not username: return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return None
    perm = Permissions.objects.filter(user=user.first())
    if not perm.exists(): return None
    return json.dumps({x: y for x, y in perm.values('errorsreport').first().items()})
