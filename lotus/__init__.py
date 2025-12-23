from __future__ import absolute_import, unicode_literals
import os

if not (os.getenv('VERCEL') == '1' or os.getenv('VERCEL')):
    from .celery import app as celery_app
    __all__ = ('celery_app',)
else:
    __all__ = tuple()