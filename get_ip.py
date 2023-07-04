import socket


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


# print(get_ip_address())
from urllib.request import urlopen
import re as r


def getIP():
    d = str(urlopen("http://checkip.dyndns.com/").read())

    return r.compile(r"Address: (\d+\.\d+\.\d+\.\d+)").search(d).group(1)


print(getIP())
