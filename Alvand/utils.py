import socket, time, os, datetime, itertools
from django.utils import timezone
from django.db.models import F, Case, When, Value
from .models import Faults, Records, ArrayAppend


def telnetConnection(attempts=3, port: int = 2300, network_id: str = "192.168.1.100"):
    port = port
    ip = network_id
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return sock
    except Exception as err:
        if attempts > 0:
            attempts -= 1
        else:
            attempts = 3
        if err != "[WinError 10061] No connection could be made because the target machine actively refused it":
            time.sleep(3)
            return telnetConnection(attempts - 1, port=port, network_id=ip)


class SocketReader:
    def __init__(self):
        self.buffer = b''

    def read_until(self, sock: socket.socket, delimiter: bytes, bs=1024) -> bytes:
        while delimiter not in self.buffer:
            chunk = sock.recv(bs)
            if not chunk:
                # TODO: MAKE NOTICE TO CHECK NETWORK CABLE (NETWORK CABLE DISCONNECTED)
                return b''
            self.buffer += chunk
        data, self.buffer = self.buffer.split(delimiter, 1)
        return data + delimiter


def parseDate(date_str):
    parts = list(map(int, date_str.split('/')))
    if len(parts) != 3:
        return datetime.date.today()
    valid_options = []
    for perm in set(itertools.permutations(parts)):
        day, month, year = perm
        if not (1 <= month <= 12):
            continue
        year_adj = year + 2000 if year < 100 else year
        try:
            d = datetime.datetime(year_adj, month, day)
        except ValueError:
            continue
        score = 0
        if perm[1] == parts[1]:
            score += 10
        if perm[2] == parts[2] and parts[2] > 12:
            score += 10
        valid_options.append((score, d, perm))
    if not valid_options:
        return datetime.date.today()
    valid_options.sort(key=lambda x: (x[0], x[1].year, x[1].month, x[1].day), reverse=True)
    best_date = valid_options[0][1]
    return best_date

def parseTime(time_str):
    parts = list(map(int, time_str.split(":")))
    ntime = datetime.datetime.now().time()
    if len(parts) != 2:
        return datetime.time(ntime.hour, ntime.minute)
    return datetime.time(parts[0], parts[1])


def returnNumber(string):
    if string.find(".") != -1:
        return "SECRET"
    string = string if string.find("<I>") == -1 else string.replace("<I>", "")
    if not string.startswith("+") or not string.startswith("00"):
        if not string.startswith("+98") and not string.startswith("0098"): string = "+98" + string[
                                                                                            1:] if string.startswith(
            "0") else string
    return string

def checkIfValidData(string):
    check = all(field not in string for field in
                ['Date', 'Time', 'Ext', 'CO', 'Dial', 'Dial Number', 'Ring Duration', 'Call Duration', 'Cost',
                 'Acc Code'])
    if check:
        if string.strip().replace("-", "") != "":
            return True
    return False

def isEthernetPort(name):
    return "ethernet" in name.lower().replace(" ", "")


def isDuration(string):
    return string.replace("'", ":") if len(string.split("'")[0]) != 1 else None


def isBeep(string):
    return string.replace("'", ":") if len(string.split("'")[0]) == 1 else None


def processToCheckEverything(string: str):
    if isinstance(string, bytes):
        string = string.decode("utf-8")
    string = string.replace("-", "")
    path = os.path.join("records")
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{datetime.datetime.now().strftime('%Y-%m')}.txt", 'a+', encoding="utf-8") as file:
        file.write(f"record ~> {string}\n")
    spliting = string.split()
    spliting[0] = parseDate(spliting[0])
    spliting[1] = parseTime(spliting[1].lower().replace("pm", "").replace("am", ""))
    mixDateTime = timezone.make_aware(datetime.datetime.strptime(f"{spliting[0].year}/{spliting[0].month}/{spliting[0].day} {spliting[1].hour}:{spliting[1].minute}", "%Y/%m/%d %H:%M"), timezone.get_current_timezone())
    mixDate = timezone.make_aware(spliting[0], timezone.get_current_timezone())
    mixTime = timezone.make_aware(spliting[1], timezone.get_current_timezone())
    if string.find("ALM") != -1:
        Faults.objects.create(date_time=mixDateTime, errorcode=int(string[26:29]))
        print("Error:", string)
        print("ERROR CODE:", string[26:29])
    else:
        if string.find("<D>") != -1:
            string = string.replace("<D>", "")
        print(spliting)
        if string.find("<I>") != -1:
            beep = isBeep(spliting[5]) if len(spliting) - 1 >= 5 else None
            duration = isDuration(spliting[6]) if len(spliting) - 1 >= 6 else None
            print("string:", string)
            if string.find("NA") != -1:
                callType = 'incomingNA'
                check = Records.objects.filter(extension=spliting[2], urbanline=spliting[3],
                                               contactnumber=returnNumber(spliting[4]), calltype='incomingRC')
                if check.exists():
                    check.update(calltype=callType, beepsnumber=beep, durationtime=duration, updated_at=timezone.now())
                else:
                    Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                           contactnumber=returnNumber(spliting[4]), calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                print("NA:", string)
            elif string.find("RC") != -1:
                callType = 'incomingRC'
                Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                       contactnumber=returnNumber(spliting[4]), calltype=callType,
                                       urbanline=spliting[3], beepsnumber=None, durationtime=None)

                print("Received Call", string)
            elif string.find("AN") != -1:
                callType = 'incomingAN'
                check = Records.objects.filter(extension=spliting[2], urbanline=spliting[3],
                                               contactnumber=returnNumber(spliting[4]), calltype='incomingRC')
                if check.exists():
                    check.update(calltype=callType, beepsnumber=beep, updated_at=timezone.now())
                else:
                    Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                           contactnumber=returnNumber(spliting[4]), calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                print("CHECK AN:", check)
                print("Incoming with anwser:", string)
            elif string.find("TR") != -1:
                callType = "Transfer"
                check = Records.objects.filter(internal=int(spliting[2]), calltype__in=['incomingHangUp', callType], contactnumber=returnNumber(spliting[4]))
                print(check)
                if check.exists():
                    check.update(transferring=Case(
                        When(transferring=None, then=Value([])),
                        default=ArrayAppend(F('transferring'), Value(spliting[2]))
                    ), durationtime=duration, calltype=callType)
                else:
                    Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                           contactnumber=returnNumber(spliting[4]), calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                    print(check)
                print("Transferring call from {} to {}".format(check[0][0] if check else None, spliting[2]))
            elif string.find("D0") != -1:
                callType = "incomingDISA"
                Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                       contactnumber=returnNumber(spliting[4]), calltype=callType,
                                       urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                print("Incoming DISA:", string)
            else:
                callType = 'incomingHangUp'
                check = Records.objects.filter(extension=spliting[2], urbanline=spliting[3],
                                               contactnumber=returnNumber(spliting[4]), calltype=callType)
                if check.exists():
                    check.update(calltype=callType, beepsnumber=beep, durationtime=duration, updated_at=timezone.now())
                else:
                    Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                           contactnumber=returnNumber(spliting[4]), calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                print("Incoming hangup with anwser:", string)
        else:
            if string.find("EXT") != -1:
                beep = isBeep(spliting[5]) if len(spliting) - 1 >= 5 else None
                duration = isDuration(spliting[6]) if len(spliting) - 1 >= 6 else None
                callType = 'Extension'
                anotherExt = int(spliting[3].replace("EXT", ""))
                val = str(anotherExt) if str(anotherExt) != str(spliting[2]) else None
                check = Records.objects.filter(calltype=callType, extension=spliting[2], internal=anotherExt)
                if check.exists():

                    check.update(transferring=Case(
                        When(transferring=None, then=Value([])),
                        default=ArrayAppend(F('transferring'), Value(val))
                    ))
                else:
                    Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                           calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration, internal=val)
                print("Extension:", string)
            else:
                duration = isDuration(spliting[6]) if len(spliting) - 1 >= 6 else None
                callType = 'outGoing'
                print("Out:", string)
                Records.objects.create(date=mixDate, hour=mixTime, extension=spliting[2],
                                       contactnumber=returnNumber(spliting[4]), calltype=callType,
                                       urbanline=spliting[3], beepsnumber=None, durationtime=duration)
    return True
