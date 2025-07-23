from .models import Users, Infos

def getTupleIndex(tuple, value):
    for i, val in enumerate(tuple):
        if val[0] == value:
            return val[1]
    return -1

def getUserinfoByUsername(username, value):
    if not isinstance(username, str):
        return None
    user = Users.objects.filter(username__iexact=username)
    if not user.exists():
        return None
    qs = Infos.objects.filter(user=user.first())
    if not qs.exists():
        return None
    return next(iter(qs.values(value).first().values()))
