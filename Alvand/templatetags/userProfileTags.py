from django.template import Library
from Alvand.models import Groups, Users, Infos, Permissions
from Alvand.views import getUserinfoByUsername
import json
register = Library()

@register.filter
def getGroupName(_id, value):
    if not isinstance(_id, int): return None
    group = Groups.objects.filter(id=_id)
    if not group.exists(): return None
    if not value in group.values().first(): return None
    return next(iter(group.values(value).first().values()))

@register.filter
def getObjectOfInfo(username):
    if not isinstance(username, str): return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return None
    qs = Infos.objects.filter(user=user.first())
    if not qs.exists(): return None
    return qs

@register.filter
def getListOfExtsGroups(username):
    if not isinstance(username, str): return []
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return []
    perm = Permissions.objects.filter(user=user.first())
    if not perm.exists(): return []
    return perm.first().exts_label

@register.filter
def getUserCanPerm(username):
    if not isinstance(username, str): return {}
    user = Users.objects.filter(username__iexact=username)
    if not user.exists(): return {}
    perm = Permissions.objects.filter(user=user.first())
    if not perm.exists(): return {}
    return json.dumps({x: y for x, y in perm.values('can_view', 'can_write', 'can_modify', 'can_delete').first().items()})

@register.filter
def getUserInfo(username, value):
    getInfo = getUserinfoByUsername(username, value)
    return getInfo if getInfo else ""