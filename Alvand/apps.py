import os
import time

from django.apps import AppConfig
from subprocess import Popen, DEVNULL
import psutil

IS_VERCEL = os.getenv('VERCEL') == '1' or os.getenv('VERCEL')

celery = os.path.join('celery')
if not IS_VERCEL:
    try:
        os.makedirs(celery, exist_ok=True)
    except OSError:
        import tempfile
        celery = os.path.join(tempfile.gettempdir(), 'celery')
        os.makedirs(celery, exist_ok=True)
else:
    # On Vercel, use /tmp as a fallback path even though we shouldn't be writing
    import tempfile
    celery = os.path.join(tempfile.gettempdir(), 'celery')

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
    if IS_VERCEL:
        return
    print("Starting Celery Worker...")
    Popen(['celery', '-A', 'lotus', 'worker', '--pool=gevent', '--loglevel=INFO'],
          stdout=open(os.path.join(celery, 'celery_worker.log'), 'w'), stderr=open(os.path.join(celery, 'celery_worker_err.log'), 'w'), shell=True)


def beatTask():
    if IS_VERCEL:
        return
    if not any(p.info["cmdline"] and "celery" in p.info["cmdline"] and "beat" in p.info["cmdline"]
               for p in psutil.process_iter(attrs=["cmdline"])):
        print("Starting Celery Beat...")
        Popen(['celery', '-A', 'lotus', 'beat', '--loglevel=INFO'],
              stdout=open(os.path.join(celery, 'celery_beat.log'), 'w'), stderr=open(os.path.join(celery, 'celery_beat_err.log'), 'w'), shell=True)




class AlvandConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Alvand'

    def ready(self):
        if IS_VERCEL:
            return
        if os.environ.get("RUN_MAIN") == 'true':
            print(isCeleryRunning())
            if not isCeleryRunning():startTask()
            time.sleep(3)
            beatTask()