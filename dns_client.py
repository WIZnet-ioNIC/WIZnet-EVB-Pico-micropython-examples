from w5x00 import w5x00_init
import usocket
import time
from machine import Pin

led = Pin(25, Pin.OUT)
"""
DNS Domain Name Resolution.
 
param: domain name
returns: IP Address

"""


def dns_query(domain):
    ip = usocket.getaddrinfo(domain, 80, 0, usocket.SOCK_STREAM)
    return ip[0][4][0]


def main():
    print("WIZnet chip DNS example")
    domain = "www.wiznet.io"

    w5x00_init()
    ip = dns_query(domain)
    print("IP address of %s is %s" % (domain, ip))

    while True:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)


if __name__ == "__main__":
    main()
