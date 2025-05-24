from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import os, json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lotus.settings')

app = Celery('lotus')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_connection_retry_on_startup = True

@app.on_after_finalize.connect
def setupPeriodicTask(sender: Celery, **kwargs):
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10, period=IntervalSchedule.SECONDS
    )
    schedule2, created2 = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.HOURS
    )# 2592000 1M
    schedule3, created3 = IntervalSchedule.objects.get_or_create(
        every=3, period=IntervalSchedule.MINUTES
    )
    tasks = [
        ("checkCOMPorts", "Alvand.tasks.checkCOMPorts"),
        ("checkNetworkStatus", "Alvand.tasks.checkNetworkStatus"),
        ("sendFaultsToEmail", "Alvand.tasks.sendFaultsToEmail"),
        ("sendInfos", "Alvand.tasks.sendInfos"),
        ("connectToDevice", "Alvand.tasks.connectToDevice"),
    ]
    for name, task in tasks:
        obj, created = PeriodicTask.objects.get_or_create(
            name=name,
            defaults={"task": task, "interval": schedule if name != "sendFaultsToEmail" else schedule2 if name == "sendFaultsToEmail" else schedule3, "enabled": True, "args": json.dumps([])}
        )
        if not created and not obj.enabled:
            obj.enabled = True
            obj.save()
