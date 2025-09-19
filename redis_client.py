# ===== Net Config (edit here) =====
BOARD    = "W6300-EVB-Pico2"  # Board name is case-insensitive
USE_DHCP = True

# Static IP settings (used when USE_DHCP=False)
NET_IP   = "192.168.11.20"
NET_SN   = "255.255.255.0"
NET_GW   = "192.168.11.1"
NET_DNS  = "8.8.8.8"
# ==================================

from usocket import socket, AF_INET, SOCK_DGRAM, getaddrinfo
from wiznet_init import wiznet
from picoredis import Redis


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
    if USE_DHCP:
        nic = wiznet(BOARD, dhcp=True)
    else:
        nic = wiznet(BOARD, dhcp=False, ip=NET_IP, sn=NET_SN, gw=NET_GW, dns=NET_DNS)

    # redis test
    redis_test()


if __name__ == "__main__":
    main()
