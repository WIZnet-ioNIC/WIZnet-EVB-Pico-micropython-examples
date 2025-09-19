# ===== Net Config (edit here) =====
BOARD    = "W6300-EVB-Pico2"  # Board name is case-insensitive
MODE     = 0                  # 0: "server", 1: "client"
USE_DHCP = False

# Static IP settings (used when USE_DHCP=False)
NET_IP   = "192.168.11.20"
NET_SN   = "255.255.255.0"
NET_GW   = "192.168.11.1"
NET_DNS  = "8.8.8.8"

# TCP settings
LOCAL_PORT  = 5000
DEST_IP     = "192.168.11.2"
DEST_PORT   = 5000
# ==================================

from usocket import socket, SOL_SOCKET, SO_REUSEADDR
import uerrno as errno
from wiznet_init import wiznet

def server_loop(nic=None):
    s = socket()
    try:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    except Exception:
        pass

    # Decide bind address
    ip_addr = nic.ifconfig()[0] if nic else NET_IP

    s.bind((ip_addr, LOCAL_PORT))
    s.listen(5)
    print("TEST server on {}:{}".format(ip_addr, LOCAL_PORT))

    try:
        conn, addr = s.accept()
        print("Connected:", addr)
        print("Loopback server Open!")
    # Set timeout if needed (e.g., 30 seconds)
    # conn.settimeout(30)
        while True:
            data = conn.recv(2048)
            if not data:
                # Peer closed the socket gracefully
                raise OSError(errno.ECONNRESET, "peer closed")
            print(data.decode("utf-8", "ignore"))
            if data != b"NULL":
                conn.send(data)

    except OSError as e:
        # Log and exit on fatal network error
        print("Server error:", e)
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass
        s.close()

def client_loop():
    s = socket()
    # Set timeout if needed (e.g., 30 seconds)
    try:
        print("Connecting to {}:{}".format(DEST_IP, DEST_PORT))
        s.connect((DEST_IP, DEST_PORT))
        print("Loopback client Connect!")
        while True:
            data = s.recv(2048)
            if not data:
                # Server closed the connection
                raise OSError(errno.ECONNRESET, "server closed")
            print(data.decode("utf-8", "ignore"))
            if data != b"NULL":
                s.send(data)
    except OSError as e:
        print("Client error:", e)
        raise
    finally:
        s.close()

def main():
    if USE_DHCP:
        nic = wiznet(BOARD, dhcp=True)
    else:
        nic = wiznet(BOARD, dhcp=False, ip=NET_IP, sn=NET_SN, gw=NET_GW, dns=NET_DNS)

    if MODE == 0:
        server_loop(nic)
    elif MODE == 1:
        client_loop()
    else:
        raise ValueError("Invalid MODE, use 'server' or 'client'")

if __name__ == "__main__":
    main()
