from usocket import socket, AF_INET, SOCK_DGRAM, getaddrinfo
from machine import Pin, WIZNET_PIO_SPI
import network
import time
import struct

from picoredis import Redis

# W5x00 chip initialization
def w5x00_init(ip_info=None):
    # ip_info = ('192.168.11.20','255.255.255.0','192.168.11.1','8.8.8.8')
    spi = WIZNET_PIO_SPI(baudrate=31_250_000, mosi=Pin(23), miso=Pin(22), sck=Pin(21))  # W55RP20 PIO_SPI
    nic = network.WIZNET5K(spi, Pin(20), Pin(25))  # spi, cs, reset pin
    nic.active(True)
    delay = 1
    
    if ip_info:
        # Static IP
        nic.ifconfig(ip_info)
    else:
        # DHCP
        for i in range(5):  # DHCP sometimes fails, so we try multiple attempts
            try:
                nic.ifconfig('dhcp')
            except Exception as e:
                print(f"Attempt {i + 1} failed, retrying in {delay} second(s)...")
            time.sleep(delay)
    
    while not nic.isconnected():
        print("Waiting for the network to connect...")
        time.sleep(1)
        # print(nic.regs())
    
    print('IP Address:', nic.ifconfig())
    return nic


def redis_test():
    redis = Redis('redis server ip address', port=6379, debug=False)
    response = redis.ping()
    print(response.decode())
    response = redis.ping("os")
    print(response.decode())
    response = redis.set("pico", "test from pico")
    print(response)
    response = redis.get("pico")
    print(response)
    

def main():
    nic = w5x00_init()

    # redis test
    redis_test()


if __name__ == "__main__":
    main()
