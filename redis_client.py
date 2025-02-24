from usocket import socket, AF_INET, SOCK_DGRAM, getaddrinfo
from machine import Pin, WIZNET_PIO_SPI
import network
import time
import struct

from picoredis import Redis
from w5x00 import w5x00_init


def redis_test():
    redis = Redis("redis server ip address", port=6379, debug=False)
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
