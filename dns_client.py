# ===== Net Config (edit here) =====
BOARD    = "W6300-EVB-Pico2"  # Board name is case-insensitive
DOMAIN   = "www.wiznet.io"                  # 0: "server", 1: "client"
USE_DHCP = False

# Static IP settings (used when USE_DHCP=False)
NET_IP   = "192.168.11.20"
NET_SN   = "255.255.255.0"
NET_GW   = "192.168.11.1"
NET_DNS  = "8.8.8.8"
# ==================================

import usocket
import time
from machine import Pin
from wiznet_init import wiznet

led = Pin("LED", Pin.OUT)
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
    domain = DOMAIN

    if USE_DHCP:
        nic = wiznet(BOARD, dhcp=True)
    else:
        nic = wiznet(BOARD, dhcp=False, ip=NET_IP, sn=NET_SN, gw=NET_GW, dns=NET_DNS)

    ip = dns_query(domain)
    print("IP address of %s is %s" % (domain, ip))

    while True:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)

if __name__ == "__main__":
    main()

