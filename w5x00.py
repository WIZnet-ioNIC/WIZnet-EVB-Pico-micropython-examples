"""
# 사용 예시:

from w5x00 import w5x00_init

# 1. DHCP를 사용하여 네트워크 초기화
nic = w5x00_init()

# 2. 고정 IP를 사용하여 네트워크 초기화
ip_info = ('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
nic = w5x00_init(ip_info=ip_info, use_dhcp=False)

# 3. DHCP를 사용하지 않고 기본 고정 IP로 네트워크 초기화
nic = w5x00_init(use_dhcp=False)

# 초기화된 네트워크 인터페이스 사용
print(nic.ifconfig())  # 현재 네트워크 설정 출력

# 주의: w5x00_init 함수는 네트워크 연결이 설정될 때까지 대기합니다.
# 따라서 이 함수 호출 후에는 네트워크가 이미 연결된 상태입니다.
"""

from machine import Pin, WIZNET_PIO_SPI
import network
import time


# W5x00 chip initialization
def w5x00_init(ip_info=None, use_dhcp=True):
    # ip_info = ('192.168.11.20','255.255.255.0','192.168.11.1','8.8.8.8')
    spi = WIZNET_PIO_SPI(
        baudrate=31_250_000, mosi=Pin(23), miso=Pin(22), sck=Pin(21)
    )  # W55RP20 PIO_SPI
    nic = network.WIZNET5K(spi, Pin(20), Pin(25))  # spi, cs, reset pin
    nic.active(True)
    delay = 1

    if ip_info:
        # Static IP
        nic.ifconfig(ip_info)
    elif not use_dhcp:
        # None DHCP
        nic.ifconfig(("192.168.11.20", "255.255.255.0", "192.168.11.1", "8.8.8.8"))
    else:
        # DHCP
        for i in range(5):  # DHCP sometimes fails, so we try multiple attempts
            try:
                nic.ifconfig("dhcp")
            except Exception as e:
                print(
                    f"Attempt {i + 1} failed, retrying in {delay} second(s)...{type(e)}"
                )
            time.sleep(delay)

    while not nic.isconnected():
        print("Waiting for the network to connect...")
        time.sleep(1)
        print(nic.regs())

    print("MAC Address:", ":".join("%02x" % b for b in nic.config("mac")))
    print("IP Address:", nic.ifconfig())
    return nic


def main():
    nic = w5x00_init()
    print(nic.ifconfig())


if __name__ == "__main__":
    main()
