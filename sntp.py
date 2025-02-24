from usocket import socket, AF_INET, SOCK_DGRAM, getaddrinfo
from machine import Pin, WIZNET_PIO_SPI
import network
import time
import struct
from w5x00 import w5x00_init


# Function to synchronize time from the SNTP server
def sntp_request(nic):
    NTP_SERVER = "pool.ntp.org"
    # NTP_SERVER = "time.google.com"
    # NTP_SERVER = "debian.pool.ntp.org"
    NTP_PORT = 123
    NTP_PACKET_FORMAT = (
        "!BbBb11I"  # ! Big-endian, NTP header 1B, Stratum 1B, Poll 1B, Precision 1B
    )
    NTP_DELTA = 2208988800  # Difference between NTP timestamp and Unix timestamp

    # Create a UDP socket
    print("Setting up UDP socket...")
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(5)  # Set a 5-second timeout

    print("Creating SNTP request packet...")
    # Create SNTP request packet (no leap second, version 4, mode 3)
    packet = struct.pack(NTP_PACKET_FORMAT, 0b00100011, 0, 0, 0, *(0,) * 11)
    # 0b(LI=00, VN=100, Mode=011), stratum, poll, precision, root delay 4B, root dispersion 4B, reference identifier 4B
    # LI (Leap Indicator): 00 = no leap second, 01 = 61 seconds, 10 = 59 seconds, 11 = unsynchronized
    # VN (Version Number): NTP version. As of 2024.10.08, version 4
    # Mode: NTP packet mode 000: Reserved, 001: Symmetric active, 010: Symmetric passive, 011: Client, 100: Server, 101: Broadcast, 110: NTP control message, 111: Reserved for private use

    try:
        print("Resolving NTP server address...")
        # Get the SNTP server address
        addr = getaddrinfo(NTP_SERVER, NTP_PORT)[0][-1]
        print(f"Sending NTP request to {NTP_SERVER} ({addr})")

        # Send SNTP request
        sock.sendto(packet, addr)

        print("Waiting for SNTP response...")
        # Receive SNTP response
        data, _ = sock.recvfrom(48)

        print("SNTP response received!")
        # Extract time from received data (32-bit integer, in seconds)
        t = struct.unpack("!12I", data)[10] - NTP_DELTA
        print("NTP Time (UTC):", time.localtime(t))

    except Exception as e:
        print("NTP request timed out.", e)

    finally:
        sock.close()


def main():
    nic = w5x00_init()

    # Send SNTP time synchronization request
    sntp_request(nic)


if __name__ == "__main__":
    main()
