from django.template import Library
from Alvand.models import Groups, Users, Infos, Permissions, Extensionsgroups
from Alvand.user_utils import getUserinfoByUsername
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
def hasErrorsAccess(username):
    """Return True if the user has permission to view the errors report page."""
    if not isinstance(username, str):
        return False
    user = Users.objects.filter(username__iexact=username).first()
    if not user:
        return False
    
    # Supporter users have full access - bypass permission checks
    if user.groupname.lower() == "supporter":
        return True
    
    perm = Permissions.objects.filter(user=user).first()
    return bool(perm and getattr(perm, 'errorsreport', False))

@register.filter
def getUserInfo(username, value):
    getInfo = getUserinfoByUsername(username, value)
    return getInfo if getInfo else ""

@register.filter
def needsPasswordChange(username):
    if not isinstance(username, str):
        return False
    user = Users.objects.filter(username__iexact=username).first()
    if not user:
        return False
    return bool(getattr(user, 'needs_password_change', False))

@register.filter
def getUserExtensions(username):
    """برگرداندن لیست داخلی‌هایی که کاربر به آن‌ها دسترسی دارد."""
    if not isinstance(username, str):
        return []

    user = Users.objects.filter(username__iexact=username).first()
    if not user:
        return []

    exts = set()

    # داخلی اصلی کاربر
    if getattr(user, 'extension', None):
        exts.add(str(user.extension))

    # داخلی‌های اضافی تعریف‌شده برای کاربر
    user_exts = getattr(user, 'usersextension', None)
    if user_exts:
        for e in user_exts:
            if e:
                exts.add(str(e))

    # داخلی‌های ناشی از گروه‌های داخلی (Extensionsgroups)
    perm = Permissions.objects.filter(user=user).first()
    if perm and getattr(perm, 'exts_label', None):
        groups_qs = Extensionsgroups.objects.filter(label__in=perm.exts_label)
        for g in groups_qs:
            if g.exts:
                for e in g.exts:
                    if e:
                        exts.add(str(e))

    # برگرداندن لیست مرتب‌شده (به صورت رشته)
    try:
        return sorted(exts, key=lambda x: int(x))
    except ValueError:
        return sorted(exts)