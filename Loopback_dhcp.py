from usocket import socket
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

    print("MAC Address:", ':'.join('%02x' % b for b in nic.config('mac')))
    print("IP Address:", nic.ifconfig())
    return nic


def server_loop(nic=None):
    s = socket()
    ip_addr = "192.168.11.20"
    port = 5000
    if nic:
        ip_addr = nic.ifconfig()[0]
    # s.bind(("192.168.11.20", 5000))  # Source IP Address
    s.bind((ip_addr, port))
    s.listen(5)

    print("TEST server")
    conn, addr = s.accept()
    print("Connect to:", conn, "address:", addr)
    print("Loopback server Open!")
    while True:
        data = conn.recv(2048)
        print(data.decode("utf-8"))
        if data != "NULL":
            conn.send(data)


def client_loop():
    s = socket()
    s.connect(("192.168.11.2", 5000))  # Destination IP Address

    print("Loopback client Connect!")
    while True:
        data = s.recv(2048)
        print(data.decode("utf-8"))
        if data != "NULL":
            s.send(data)


def main():
    nic = w5x00_init()

    ###TCP SERVER###
    server_loop(nic)

    ###TCP CLIENT###
    # client_loop()


if __name__ == "__main__":
    main()
