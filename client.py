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

if __name__ == "__main__":
    data = needData("127.0.0.1", '3C521D01-517C-11CB-AD31-9C9ABC89A6FB')
    try:
        data = json.loads(data)
    except:
        data = data
    check = checkLicense("127.0.0.1", 'pbkdf2_sha256$870000$KODpUJ3KtpafPH89j6UDzn$PkwksVhZz11ZO5Ph99GiGVdn3BVesyg6rtO1jdcYVRE=')
    check1 = checkLicense("127.0.0.1", 'pbkdf2_sha256$870000$KODpUJ3KtpafPH89j6UDzn$PkwkdsVhZz11ZO5Ph99GiGVdn3BVesyg6rtO1jdcYVRE=')
    breakpoint()