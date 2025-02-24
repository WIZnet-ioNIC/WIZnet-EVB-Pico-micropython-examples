from usocket import socket
from machine import Pin, WIZNET_PIO_SPI
import urequests
import network
import time
from w5x00 import w5x00_init


def request():
    r = urequests.get("http://httpbin.org/get")
    # r.raise_for_status
    print(r.status_code)
    print(r.text)
    r = urequests.post("http://httpbin.org/post", json={"WIZnet Test"})
    if not r:
        print("spreadsheet: no response received")
    print(r.json())


def main():
    w5x00_init()
    request()


if __name__ == "__main__":
    main()
