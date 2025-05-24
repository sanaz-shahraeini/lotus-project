import os
import time

from django.apps import AppConfig
from subprocess import Popen, DEVNULL
import psutil

celery = os.path.join('celery')
os.makedirs(celery, exist_ok=True)

def isCeleryRunning():
    for p in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        try:
            name = p.info.get("name", "").lower()
            cmdline = p.info.get("cmdline") or []
            if (name and "celery" in name) or any("celery" in part for part in cmdline):
                print(f"Celery is already running - PID: {p.info['pid']}, Name: {name}, Cmdline: {cmdline}")
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as err:
            print(err)
            continue

    return False



def startTask():
    print("Starting Celery Worker...")
    Popen(['celery', '-A', 'lotus', 'worker', '--pool=gevent', '--loglevel=INFO'],
          stdout=open('celery/celery_worker.log', 'w'), stderr=open('celery/celery_worker_err.log', 'w'), shell=True)


def beatTask():
    if not any(p.info["cmdline"] and "celery" in p.info["cmdline"] and "beat" in p.info["cmdline"]
               for p in psutil.process_iter(attrs=["cmdline"])):
        print("Starting Celery Beat...")
        Popen(['celery', '-A', 'lotus', 'beat', '--loglevel=INFO'],
              stdout=open('celery/celery_beat.log', 'w'), stderr=open('celery/celery_beat_err.log', 'w'), shell=True)




class AlvandConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Alvand'

    def ready(self):
        if os.environ.get("RUN_MAIN") == 'true':
            print(isCeleryRunning())
            if not isCeleryRunning():startTask()
            time.sleep(3)
            beatTask()