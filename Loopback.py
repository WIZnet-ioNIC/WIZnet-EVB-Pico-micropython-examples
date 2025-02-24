from usocket import socket
from machine import Pin, WIZNET_PIO_SPI
import network
import time
from w5x00 import w5x00_init


def server_loop():
    s = socket()
    s.bind(("192.168.11.20", 5000))  # Source IP Address
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
    w5x00_init()

    ###TCP SERVER###
    # server_loop()

    ###TCP CLIENT###
    client_loop()


if __name__ == "__main__":
    main()
