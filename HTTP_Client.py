# ===== Net Config (edit here) =====
BOARD    = "W6300-EVB-Pico2"  # Board name is case-insensitive
USE_DHCP = False

# Static IP settings (used when USE_DHCP=False)
NET_IP   = "192.168.11.20"
NET_SN   = "255.255.255.0"
NET_GW   = "192.168.11.1"
NET_DNS  = "8.8.8.8"

URL      = "http://httpbin.org"
# ==================================

from usocket import socket
import urequests
from wiznet_init import wiznet

def request(url: str):
    r = urequests.get(f"{url}/get")
    # r.raise_for_status
    print(r.status_code)
    print(r.text)
    r = urequests.post(f"{url}/post", json={"WIZnet Test"})
    if not r:
        print("spreadsheet: no response received")
    print(r.json())

def main():
    if USE_DHCP:
        nic = wiznet(BOARD, dhcp=True)
    else:
        nic = wiznet(BOARD, dhcp=False, ip=NET_IP, sn=NET_SN, gw=NET_GW, dns=NET_DNS)

    request(URL)

if __name__ == "__main__":
    main()
