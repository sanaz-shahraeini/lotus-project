import socket

from django.core.cache import cache
from celery import shared_task
from .utils import telnetConnection, SocketReader, isEthernetPort, checkIfValidData, processToCheckEverything
from .models import Device, errorsSent, Faults, Emailsending, lices, Users, Infos
from django.db.models import OuterRef, Subquery
from .views import sendEmail, getHWID, log, logMessages, logErrCodes
import serial, serial.tools.list_ports, psutil, time
from checkLicense import updateData


class successSent:
    success = 0
    unsuccess = 1
    unverified = 2
    usernotfound = 3
    adminnotfound = 4

@shared_task
def checkCOMPorts():
    # print("CALLED checkCOMPorts")
    if True: return
    previous_ports = cache.get("com_ports", {})
    current_ports = {port.device: port.description for port in serial.tools.list_ports.comports()}
    new_ports = set(current_ports) - set(previous_ports)
    removed_ports = set(previous_ports) - set(current_ports)
    portConnected = cache.get("portConnected", {})
    # print("CURRENT PORTS:", current_ports)
    # print("NEW PORTS:", new_ports)
    if new_ports:
        for port in new_ports:
            if "modem" not in current_ports[port].lower() and port not in portConnected:
                getDeviceInfo = Device.objects.all()
                if not getDeviceInfo.exists():
                    portConnected[port] = {"baudrate": 19200, "parity": serial.PARITY_NONE,
                                           "stopbits": serial.STOPBITS_ONE, "databits": serial.EIGHTBITS, "flow": None}
                else:
                    portConnected[port] = {"baudrate": int(getDeviceInfo.first().baudrate),
                                           "parity": getDeviceInfo.first().parity,
                                           "stopbits": getDeviceInfo.first().stopbits,
                                           "databits": getDeviceInfo.first().databits,
                                           "flow": getDeviceInfo.first().flow if getDeviceInfo.first().flow and getDeviceInfo.first().flow.lower() != "none" else None}

    for port in removed_ports:
        portConnected.pop(port, None)

    cache.set("com_ports", current_ports)
    cache.set("portConnected", portConnected)
    return "checkCOMPORTS"


@shared_task
def checkNetworkStatus():
    previous_status = cache.get("network_status", {})
    portConnected = cache.get("portConnected", {})
    for nic in psutil.net_if_addrs():
        if isEthernetPort(nic):
            nic_info = psutil.net_if_stats().get(nic)
            portConnected[nic] = nic_info.isup if nic_info else False

    if portConnected != previous_status:
        cache.set("portConnected", portConnected)
    return "checkNetworkStatus"


@shared_task
def connectToDevice():
    print("CALLED SELAM connectToDevice")
    if True: return
    portConnected = cache.get("portConnected", {})
    telLogin = cache.get("telLogin", False)
    serialPort = cache.get("serialPort")

    canConnectTo = {k: v for k, v in portConnected.items() if "ethernet" in k.lower() or "COM" in k}
    print("CAN CONNECTED TO:", canConnectTo)
    if any("ethernet" in key.lower() for key in canConnectTo.keys()):
        getNetInfo = Device.objects.all()
        if getNetInfo.exists():
            if getNetInfo.first().smdrip and getNetInfo.first().smdrport:
                telnet = telnetConnection(5, port=getNetInfo.first().smdrport,
                                          network_id=getNetInfo.first().smdrip)
            else:
                telnet = telnetConnection(5)
        else:
            telnet = telnetConnection(5)
        print("TELNET:", telnet)
        if telnet and not telLogin:
            try:
                print("PRINTABLE TELNET:", telnet)
                SocketReader().read_until(telnet, b"-")
                telnet.sendall(b'SMDR\r')
                SocketReader().read_until(telnet, b"Enter Password:")
                telnet.sendall(f"{getNetInfo.first().smdrpassword}\r".encode() if getNetInfo.exists() else b"PCCSMDR\r")
                cache.set("telLogin", True)
                cache.set("telnet", telnet)
            except Exception as err:
                print("ERR CONN:", err)
                time.sleep(3)

        if telnet and telLogin:
            try:
                command = SocketReader().read_until(telnet, b"\n")
                string = command.decode("utf-8").replace("*", "").replace("\r", "").replace("\n", "")
                print("STRING:", string)
                if checkIfValidData(string):
                    processToCheckEverything(string)
            except Exception as err:
                print("ERR TELNET CONDS:", err)
                time.sleep(1)
        else:
            cache.set("telLogin", False)

    elif any("COM" in key for key in canConnectTo.keys()):
        if serialPort and serialPort.is_open:
            serialPort.close()

        canConnectTo = [key for key in canConnectTo if "COM" in key]
        flow = portConnected[canConnectTo[0]].get("flow") or ""
        flow = flow.lower().replace("/", "")

        serial_args = {
            "port": canConnectTo[0],
            "baudrate": portConnected[canConnectTo[0]]["baudrate"],
            "bytesize": portConnected[canConnectTo[0]]["databits"],
            "parity": portConnected[canConnectTo[0]]["parity"],
            "stopbits": portConnected[canConnectTo[0]]["stopbits"]
        }

        if flow == "rtscts":
            serial_args["rtscts"] = True
        elif flow == "dsrdtr":
            serial_args["dsrdtr"] = True
        elif flow == "xonxoff":
            serial_args["xonxoff"] = True

        serialPort = serial.Serial(**serial_args)
        cache.set("serialPort", serialPort)

        while serialPort:
            if serialPort.in_waiting > 0:
                data = serialPort.readline().decode("utf-8").strip()
                if checkIfValidData(data):
                    cache.set("last_received_data", data)
    return "connectToDevice"


@shared_task
def sendFaultsToEmail():
    print('sendFaultsToEmail')
    sentFaults = errorsSent.objects.filter(fault=OuterRef('pk')).exclude(success=0).values('fault')
    faultsNotSent = Faults.objects.all().exclude(id__in=Subquery(sentFaults)).order_by('created_at')
    getEmail = Emailsending.objects.all()
    print("faults not sent:", faultsNotSent)
    print("email:", getEmail)
    if faultsNotSent.exists():
        faults = []
        for error in faultsNotSent:
            if not getEmail.exists():
                errorsSent.objects.create(fault=error, success=successSent.adminnotfound)
                continue

            if not getEmail.first().emailtosend:
                errorsSent.objects.create(fault=error, success=successSent.usernotfound)
                continue
            if error.errorcode in getEmail.first().errors:
                faults.append(error)
            # print(len(faults))
            if len(faults) >= getEmail.first().lines:
                sendErrorReport(getEmail.first(), faults)
    return "sendFaultsToEmail"


def sendErrorReport(email, faults):
    date, time, message = "", "", ""
    for item in faults:
        date = f"{item.created_at.year}/{item.created_at.month}/{item.created_at.day}"
        time = f"{item.created_at.hour}:{item.created_at.minute}"
        # 4023-24-25
        message += f"<p>خطای کد {item.errorcode} با نوع {'قابل بررسی' if item.errorcode in [5, 6] else 'عادی'} " \
                   f"در تاریخ {date} و ساعت {time} ثبت شد</p>"  # 4026
    res = sendEmail("گزارش های خطا های دریافت شده", message, [email.emailtosend], email.byadmin.username)
    for fault in faults:
        errorsSent.objects.create(fault=fault, success=successSent.success if res else successSent.unsuccess)

def sendInfos():
    try:
        ip = socket.gethostbyname("lotusiot.ir")
    except:
        ip = None
    if not ip:
        return "ipDoesnotFound"
    version = lices.objects.all()
    if not version.exists():
        return "versionNotExists"
    user = Infos.objects.filter(macaddress=getHWID())
    if not user.exists() or not user.user.exists():
        return "userNotExists"
    result = updateData("127.0.0.1", [user.user.username.lower(), user.user.name, user.user.lastname, user.phonenumber, user.user.email.lower(), user.macaddress])
    if not result:
        log(user.user.username, logErrCodes.others, logMessages.dataDidnotSend, "Lotus")
        return "dataDidNotSend"
    log(user.user.username, logErrCodes.others, logMessages.dataSent, "Lotus")
    return "sendInfos"