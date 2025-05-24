import psycopg2
from lotus import settings
from django.contrib.auth.hashers import make_password
from .models import Groups, Users, Infos, Permissions, lices
from .views import getHWID
import socket, os, json

def makeConnection(addr):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        return client
    except Exception as err:
        return f"Connection error: {err}"


def needData(host, hwid):
    conn = makeConnection((host, 1235))
    if not isinstance(conn, socket.socket):
        return f"Connection failed: {conn}"
    conn.send(f"needData;{hwid}".encode())
    result = conn.recv(4096)
    conn.close()
    return result.decode()


def checkLicense(host, lice):
    conn = makeConnection((host, 1235))
    if not isinstance(conn, socket.socket):
        return f"Connection failed: {conn}"
    conn.send(f"checkLicense;{lice}".encode())
    result = conn.recv(2048)
    conn.close()
    return True if result.decode() == 'true' else False

def updateData(host, data):
    conn = makeConnection((host, 1235))
    if not isinstance(conn, socket.socket):
        return f"Connection failed: {conn}"
    conn.send(f"updateData;{';'.join(data)}".encode())
    result = conn.recv(2048)
    conn.close()
    return True if result.decode() == "Data received" else False


def checkLicenses():
    print("CHECK LICENSES")
    try:
        superadmin_group = Groups.objects.filter(enname__iexact="superadmin").first()
        if not superadmin_group:
            print("Groups not found.")
            return None
        try:
            getIp = socket.gethostbyname("google.com")
        except Exception as err:
            getIp = None
            print(err)
        if not getIp:
            return "Connection failed"
        if getIp != settings.externalDB_ip:
            settings.externalDB_user = getIp

        result = needData(getIp)
        print(result)
        if result:
            try:
                result = json.loads(result)
            except:
                result = result
            if not result[0]:
                print("YOUR LICENSE IS NOT ACTIVE, PLEASE CONTACT WITH SUPPORTERS OR CHECK OUR WEBSITE https://lotusiot.ir")
                return False
            hw = getHWID()
            if result[8] and hw != result[8]:
                print("MAC ADDRESS DOESN'T MATCH, PLEASE CONTACT WITH SUPPORTERS")
                return False
            if not checkLicense(result[5]):
                print("INVALID LICENSE, PLEASE CONTACT WITH SUPPORTERS")
                return False
            getLices, createdLices = lices.objects.get_or_create(
                lice=result[5], active=result[0], defaults={'version': result[9]}
            )
            if getLices and not createdLices:
                getLices.update(version=result[9])
            getSuperadmin, createdSuperadmin = Users.objects.get_or_create(
                username__iexact=result[2],
                email__iexact=result[7],
                defaults={
                    "extension": 100,
                    "name": result[3],
                    "lastname": result[4],
                    "group": superadmin_group,
                    "groupname": superadmin_group.enname,
                    "email": result[7],
                    "password": make_password("123456789")
                }
            )
            Infos.objects.get_or_create(user=getSuperadmin, defaults={'macaddress': hw})
            Permissions.objects.get_or_create(user=getSuperadmin)
            return True
        else:
            print("YOU HAVE NO ANY LICENSE ACTIVATE NOW.")
            return False

    except psycopg2.Error as e:
        print(f"Error connection to db: %e")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
