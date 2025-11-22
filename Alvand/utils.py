import socket, time, os, datetime, itertools
import telnetlib
from django.utils import timezone
from django.db.models import F, Case, When, Value
from .models import Faults, Records, ArrayAppend
import threading


def telnetConnection(attempts=3, port: int = 23, network_id: str = "192.168.0.100"):
    """Open a TCP socket to the PBX SMDR port with limited retries.

    Returns a connected socket object on success, or None on failure.
    This function must NEVER block indefinitely.
    """
    ip = network_id
    last_err = None

    # Ensure we always have at least one attempt
    max_tries = attempts if isinstance(attempts, int) and attempts > 0 else 3

    for _ in range(max_tries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Avoid hanging forever if host/port is unreachable
            sock.settimeout(3)
            sock.connect((ip, int(port)))
            # Restore blocking mode for normal reads afterwards
            sock.settimeout(None)
            return sock
        except OSError as err:
            last_err = err
            # For actively refused connections, additional retries usually do not help
            if getattr(err, "errno", None) in (10061, 111):
                break
            time.sleep(3)
        except Exception as err:  # Fallback for any unexpected exception type
            last_err = err
            time.sleep(3)

    # All attempts failed
    try:
        print(f"telnetConnection: could not connect to {ip}:{port} -> {last_err}")
    except Exception:
        # Avoid raising from logging
        pass
    return None


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
    # Normalize and safely parse date strings like "1/ 3/05" or with extra spaces.
    # If parsing fails, fall back to today's date instead of raising ValueError.
    if not isinstance(date_str, str):
        return datetime.date.today()
    # Split, strip, and drop empty segments
    raw_parts = [p.strip() for p in date_str.split('/') if p.strip()]
    try:
        parts = list(map(int, raw_parts))
    except (TypeError, ValueError):
        return datetime.date.today()
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
    ntime = datetime.datetime.now().time()
    try:
        parts = list(map(int, time_str.split(":")))
    except (TypeError, ValueError):
        # Fallback to current time if parsing fails
        return datetime.time(ntime.hour, ntime.minute)
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
    """Normalize SMDR duration tokens.

    Examples:
    - "00:00'19"    -> "00:00:19"
    - "00:00'15\"" -> "00:00:15"
    - "...."         -> None (invalid placeholder)
    """
    if not isinstance(string, str):
        return None

    # Quickly reject obvious placeholders without any digits
    if not any(ch.isdigit() for ch in string):
        return None

    # Replace apostrophes with ':' and drop quotes/spaces
    s = string.strip().replace("'", ":").replace('"', "")

    # Keep only digits and ':'
    filtered = "".join(ch for ch in s if ch.isdigit() or ch == ":")
    if not filtered:
        return None

    parts = filtered.split(":")
    # Support MM:SS or HH:MM:SS
    try:
        if len(parts) == 2:
            m, sec = map(int, parts)
            h = 0
        elif len(parts) == 3:
            h, m, sec = map(int, parts)
        else:
            return None
    except ValueError:
        return None

    return f"{h:02d}:{m:02d}:{sec:02d}"


def isBeep(string):
    return string.replace("'", ":") if len(string.split("'")[0]) == 1 else None


def processToCheckEverything(string: str):
    if isinstance(string, bytes):
        string = string.decode("utf-8")
    string = string.replace("-", "")
    path = os.path.join("logs", "records")
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{datetime.datetime.now().strftime('%Y-%m')}.txt", 'a+', encoding="utf-8") as file:
        file.write(f"record ~> {string}\n")
    spliting = string.split()
    # Normalize RS232 date/time like "1/ 6/05   1:18AM" where the date is split into two tokens.
    # Example tokens: ['1/', '6/05', '1:18AM', '107', '01', '09155150730', "00:00'15\"", ...]
    # Merge the first two tokens into a proper date string before parsing.
    if len(spliting) >= 3 and "/" in spliting[0] and "/" in spliting[1] and ":" in spliting[2]:
        merged_date = f"{spliting[0]}{spliting[1]}"  # "1/" + "6/05" -> "1/6/05"
        spliting[0] = merged_date
        del spliting[1]
    spliting[0] = parseDate(spliting[0])
    spliting[1] = parseTime(spliting[1].lower().replace("pm", "").replace("am", ""))
    mixDateTime = timezone.make_aware(
        datetime.datetime.strptime(
            f"{spliting[0].year}/{spliting[0].month}/{spliting[0].day} {spliting[1].hour}:{spliting[1].minute}",
            "%Y/%m/%d %H:%M"
        ),
        timezone.get_current_timezone()
    )
    recDate = spliting[0]
    recTime = spliting[1]
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
                    Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
                                           contactnumber=returnNumber(spliting[4]), calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                print("NA:", string)
            elif string.find("RC") != -1:
                callType = 'incomingRC'
                Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
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
                    Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
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
                    Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
                                           contactnumber=returnNumber(spliting[4]), calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                    print(check)
                print("Transferring call from {} to {}".format(check[0][0] if check else None, spliting[2]))
            elif string.find("D0") != -1:
                callType = "incomingDISA"
                Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
                                       contactnumber=returnNumber(spliting[4]), calltype=callType,
                                       urbanline=spliting[3], beepsnumber=beep, durationtime=duration)
                print("Incoming DISA:", string)
            else:
                check = Records.objects.filter(extension=spliting[2], urbanline=spliting[3],
                                               contactnumber=returnNumber(spliting[4])).order_by('-id')
                if check.exists():
                    rec_obj = check.first()
                    if beep is not None:
                        rec_obj.beepsnumber = beep
                    if duration is not None:
                        rec_obj.durationtime = duration
                    rec_obj.updated_at = timezone.now()
                    rec_obj.save(update_fields=['beepsnumber', 'durationtime', 'updated_at'])
                else:
                    callType = 'incomingHangUp'
                    Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
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
                    Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
                                           calltype=callType,
                                           urbanline=spliting[3], beepsnumber=beep, durationtime=duration, internal=val)
                print("Extension:", string)
            else:
                # Handle special RS232 lines that show "<    incoming    >" instead of a dialed number.
                # These are incoming calls without CLI; treat them as incoming hangups so they appear
                # correctly as incoming in the dashboard.
                normalized = string.lower().replace(" ", "")
                if "<incoming>" in normalized:
                    # For these records, duration is usually the token before the trailing placeholder
                    # Example: 1/ 6/05   1:55AM 107  01   <    incoming    >                  00:00'45" ....
                    duration = isDuration(spliting[-2]) if len(spliting) >= 7 else None
                    callType = 'incomingHangUp'
                    contact_number = None
                    print("Incoming (no CLI):", string)
                else:
                    # Outgoing calls usually don't have a separate beep field; the last token is the duration
                    # Example: 06/01/11 15:11 101 01 09338665005 00:00'39
                    candidate = spliting[-1] if len(spliting) >= 6 else None
                    if candidate is not None and not any(ch.isdigit() for ch in candidate) and len(spliting) >= 7:
                        candidate = spliting[-2]
                    duration = isDuration(candidate) if candidate is not None else None
                    callType = 'outGoing'
                    contact_number = returnNumber(spliting[4])
                    print("Out:", string)

                Records.objects.create(date=recDate, hour=recTime, extension=spliting[2],
                                       contactnumber=contact_number, calltype=callType,
                                       urbanline=spliting[3], beepsnumber=None, durationtime=duration)
    return True


class PanasonicNS500:
    def __init__(self, host, port=23):
        self.host = host
        self.port = port
        self.connection = None

    def connect(self, username, password):
        try:
            self.connection = telnetlib.Telnet(self.host, self.port, timeout=10)

            self.connection.read_until(b"Login: ", timeout=10)
            self.connection.write(username.encode("ascii") + b"\r\n")

            self.connection.read_until(b"Password: ", timeout=10)
            self.connection.write(password.encode("ascii") + b"\r\n")

            time.sleep(2)
            response = self.connection.read_very_eager().decode("ascii", errors="ignore")

            if "Login incorrect" in response:
                raise Exception("Authentication failed")

            print("Connected successfully")
            return True

        except Exception as e:
            print(f"Connection error: {e}")
            self.connection = None
            return False

    def send_command(self, command, wait_time=2):
        if not self.connection:
            raise Exception("Not connected")

        self.connection.write(command.encode("ascii") + b"\r\n")
        time.sleep(wait_time)
        response = self.connection.read_very_eager().decode("ascii", errors="ignore")
        return response

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Disconnected")


def smdr_debug_read(host, port=23, password="PCCSMDR", max_lines=10):
    """Simple helper to debug SMDR stream over TCP.

    Connects to the PBX SMDR port, sends SMDR command and password,
    then prints up to max_lines lines of raw SMDR data.
    This function is only for manual debugging and does not touch the DB.
    """
    sock = telnetConnection(3, port=port, network_id=host)
    if not sock:
        print("Could not open socket to SMDR host")
        return

    # For debug helper, do not allow blocking forever on recv
    try:
        sock.settimeout(5)
    except Exception:
        pass

    reader = SocketReader()
    try:
        banner = reader.read_until(sock, b"-")
        print("BANNER:", banner.decode("utf-8", errors="ignore"))

        sock.sendall(b"SMDR\r")
        prompt = reader.read_until(sock, b"Enter Password:")
        print("PROMPT:", prompt.decode("utf-8", errors="ignore"))

        sock.sendall((password + "\r").encode("utf-8"))

        for i in range(max_lines):
            data = reader.read_until(sock, b"\n")
            if not data:
                break
            line = data.decode("utf-8", errors="ignore").replace("*", "").replace("\r", "").replace("\n", "")
            print(f"LINE {i+1}:", line)
    except Exception as exc:
        print("SMDR debug error:", exc)
    finally:
        try:
            sock.close()
        except Exception:
            pass

# ======================= SMDR STREAM (ETHERNET) =======================
# Simple background client to read SMDR over TCP and log/store records
_smdr_thread = None
_smdr_stop = threading.Event()

def _smdr_debug(msg: str):
         pass


def _smdr_worker(host: str, port: int, password: str):
    log_dir = os.path.join("logs", "smdr")
    os.makedirs(log_dir, exist_ok=True)
    _smdr_debug(f"Worker start host={host} port={port}")

    while not _smdr_stop.is_set():
        sock = None
        try:
            _smdr_debug("Connecting socket...")
            sock = telnetConnection(3, port=port, network_id=host)
            if not sock:
                _smdr_debug("Socket connect failed (None). Retry in 3s")
                time.sleep(3)
                continue

            reader = SocketReader()

            # Read initial banner (ends with '-') if present
            try:
                banner = reader.read_until(sock, b"-")
                _smdr_debug(f"Banner: {banner.decode('utf-8', errors='ignore')[:80]}")
            except Exception:
                _smdr_debug("No banner or read banner failed")

            # Handshake for SMDR
            try:
                _smdr_debug("Sending SMDR command")
                sock.sendall(b"SMDR\r")
                prompt = reader.read_until(sock, b"Enter Password:")
                _smdr_debug(f"Prompt: {prompt.decode('utf-8', errors='ignore')[:80]}")
                sock.sendall((password + "\r").encode("utf-8"))
                _smdr_debug("Password sent; start reading lines")
            except Exception:
                try:
                    sock.close()
                except Exception:
                    pass
                _smdr_debug("Handshake failed; retry in 2s")
                time.sleep(2)
                continue

            # Main loop: read lines
            while not _smdr_stop.is_set():
                data = reader.read_until(sock, b"\n")
                if not data:
                    _smdr_debug("Socket returned empty; break read loop")
                    break
                line = data.decode("utf-8", errors="ignore").replace("*", "").replace("\r", "").replace("\n", "")

                # Append raw line to monthly log
                try:
                    with open(os.path.join(log_dir, f"{datetime.datetime.now().strftime('%Y-%m')}.txt"), 'a+', encoding='utf-8') as f:
                        f.write(line + "\n")
                except Exception:
                    pass

                # Process valid data into DB and records log
                try:
                    if checkIfValidData(line):
                        processToCheckEverything(line)
                except Exception:
                    pass

        except Exception:
            _smdr_debug("Unexpected error in worker loop; backoff 2s")
            time.sleep(2)
        finally:
            try:
                if sock:
                    sock.close()
            except Exception:
                pass

        # Backoff before reconnect unless stop requested
        if not _smdr_stop.is_set():
            _smdr_debug("Reconnect delay 1.5s")
            time.sleep(1.5)


def start_smdr_stream(host: str, port: int = 2300, password: str = "PCCSMDR"):
    global _smdr_thread
    # Stop existing thread if running
    stop_smdr_stream()
    _smdr_stop.clear()
    _smdr_thread = threading.Thread(target=_smdr_worker, args=(host, int(port), password), daemon=True)
    _smdr_thread.start()
    _smdr_debug(f"start_smdr_stream invoked host={host} port={port}")


def stop_smdr_stream():
    global _smdr_thread
    try:
        if _smdr_thread and _smdr_thread.is_alive():
            _smdr_stop.set()
            # Give the thread a moment to exit its loop
            _smdr_thread.join(timeout=2.0)
    except Exception:
        pass
    finally:
        _smdr_stop.clear()
        _smdr_thread = None
        _smdr_debug("stop_smdr_stream invoked; state cleared")
