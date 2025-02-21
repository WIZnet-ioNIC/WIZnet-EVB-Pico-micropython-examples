from usocket import socket
from machine import Pin, WIZNET_PIO_SPI
import urequests
import network
import time
from w5x00 import w5x00_init


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
    w5x00_init()

    url = "https://httpbin.org"
    request(url)


if __name__ == "__main__":
    main()
