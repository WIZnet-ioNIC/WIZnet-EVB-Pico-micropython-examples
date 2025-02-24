from usocket import socket
from machine import Pin, WIZNET_PIO_SPI
import network
import time
from w5x00 import w5x00_init


def main():
    w5x00_init(use_dhcp=True)


if __name__ == "__main__":
    main()
