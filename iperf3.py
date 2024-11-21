"""
Pure Python, iperf3-compatible network performance test tool.

MIT license; Copyright (c) 2018-2019 Damien P. George

Supported modes: server & client, TCP & UDP, normal & reverse
modified to W55RP20: Joseph<joseph@wiznet.io>

Usage:
    import iperf3
    iperf3.server()
    iperf3.client('192.168.1.5')
    iperf3.client('192.168.1.5', udp=True, reverse=True)
"""

import json
import select
import struct
import sys
import time
from usocket import (
    socket,
    AF_INET,
    SOL_SOCKET,
    SOCK_STREAM,
    SOCK_DGRAM,
    getaddrinfo,
    SO_REUSEADDR,
    # SO_KEEPALIVESEND,
)
from machine import Pin, WIZNET_PIO_SPI
import network


# W5x00 chip initialization
def w5x00_init(ip_info=None):
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
        # print(nic.regs())

    print("IP Address:", nic.ifconfig())
    return nic


# Provide a urandom() function, supporting devices without os.urandom().
try:
    from os import urandom
except ImportError:
    from random import randint

    def urandom(n):
        return bytes(randint(0, 255) for _ in range(n))


DEBUG = False

# iperf3 cookie size, last byte is null byte
COOKIE_SIZE = 37

# iperf3 commands
TEST_START = 1
TEST_RUNNING = 2
TEST_END = 4
PARAM_EXCHANGE = 9
CREATE_STREAMS = 10
EXCHANGE_RESULTS = 13
DISPLAY_RESULTS = 14
IPERF_DONE = 16

if DEBUG:
    cmd_string = {
        TEST_START: "TEST_START",
        TEST_RUNNING: "TEST_RUNNING",
        TEST_END: "TEST_END",
        PARAM_EXCHANGE: "PARAM_EXCHANGE",
        CREATE_STREAMS: "CREATE_STREAMS",
        EXCHANGE_RESULTS: "EXCHANGE_RESULTS",
        DISPLAY_RESULTS: "DISPLAY_RESULTS",
        IPERF_DONE: "IPERF_DONE",
    }


def fmt_size(val, div):
    for mult in ("", "K", "M", "G"):
        if val < 10:
            return "% 5.2f %s" % (val, mult)
        elif val < 100:
            return "% 5.1f %s" % (val, mult)
        elif mult == "G" or val < 1000:
            return "% 5.0f %s" % (val, mult)
        else:
            val /= div


class Stats:
    def __init__(self, param):
        self.pacing_timer_us = param["pacing_timer"] * 1000
        self.udp = param.get("udp", False)
        self.reverse = param.get("reverse", False)
        self.running = False

    def start(self):
        self.running = True
        self.t0 = self.t1 = ticks_us()
        self.nb0 = self.nb1 = 0  # num bytes
        self.np0 = self.np1 = 0  # num packets
        self.nm0 = self.nm1 = 0  # num lost packets
        if self.udp:
            if self.reverse:
                extra = "         Jitter    Lost/Total Datagrams"
            else:
                extra = "         Total Datagrams"
        else:
            extra = ""
        print("Interval           Transfer     Bitrate" + extra)

    def max_dt_ms(self):
        if not self.running:
            return -1
        return max(0, (self.pacing_timer_us - ticks_diff(ticks_us(), self.t1)) // 1000)

    def add_bytes(self, n):
        if DEBUG:
            print(f"nbytes={n}")
        if not self.running:
            return
        self.nb0 += n
        self.nb1 += n
        self.np0 += 1
        self.np1 += 1

    def add_lost_packets(self, n):
        print(f"npackets={n}")
        self.np0 += n
        self.np1 += n
        self.nm0 += n
        self.nm1 += n

    def print_line(self, ta, tb, nb, np, nm, extra=""):
        dt = tb - ta
        print(
            " %5.2f-%-5.2f  sec %sBytes %sbits/sec"
            % (ta, tb, fmt_size(nb, 1024), fmt_size(nb * 8 / dt, 1000)),
            end="",
        )
        if self.udp:
            if self.reverse:
                print(
                    " %6.3f ms  %u/%u (%.1f%%)"
                    % (0, nm, np, 100 * nm / (max(1, np + nm))),
                    end="",
                )
            else:
                print("  %u" % np, end="")
        print(extra)

    def update(self, final=False):
        if not self.running:
            return
        t2 = ticks_us()
        dt = ticks_diff(t2, self.t1)
        if final or dt > self.pacing_timer_us:
            ta = ticks_diff(self.t1, self.t0) * 1e-6
            tb = ticks_diff(t2, self.t0) * 1e-6
            self.print_line(ta, tb, self.nb1, self.np1, self.nm1)
            self.t1 = t2
            self.nb1 = 0
            self.np1 = 0
            self.nm1 = 0

    def stop(self):
        self.update(True)
        self.running = False
        self.t3 = ticks_us()
        dt = ticks_diff(self.t3, self.t0)
        print("- " * 30)
        self.print_line(0, dt * 1e-6, self.nb0, self.np0, self.nm0, "  sender")

    def report_receiver(self, stats):
        st = stats["streams"][0]

        # iperf servers pre 3.2 do not transmit start or end time,
        # so use local as fallback if not available.
        dt = ticks_diff(self.t3, self.t0)

        self.print_line(
            st.get("start_time", 0.0),
            st.get("end_time", dt * 1e-6),
            st["bytes"],
            st["packets"],
            st["errors"],
            "  receiver",
        )


def recvn(s, n):
    data = b""
    while len(data) < n:
        data += s.recv(n - len(data))
    return data


def recvinto(s, buf):
    if hasattr(s, "readinto"):
        return s.readinto(buf)
    else:
        return s.recv_into(buf)


def recvninto(s, buf):
    if hasattr(s, "readinto"):
        n = s.readinto(buf)
        assert n == len(buf)
    else:
        mv = memoryview(buf)
        off = 0
        while off < len(buf):
            off += s.recv_into(mv[off:])


def make_cookie():
    cookie_chars = b"abcdefghijklmnopqrstuvwxyz234567"
    cookie = bytearray(COOKIE_SIZE)
    for i, x in enumerate(urandom(COOKIE_SIZE - 1)):
        cookie[i] = cookie_chars[x & 31]
    return cookie


def server_once():
    # Listen for a connection
    ai = getaddrinfo("0.0.0.0", 5201)
    ai = ai[0]
    print("Server listening on", ai[-1])
    s_listen = socket(ai[0], SOCK_STREAM)
    s_listen.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # s_listen.setsockopt(SOL_SOCKET, SO_KEEPALIVESEND, 1)  # Keepalive 설정 추가. 동작 안함..
    s_listen.bind(ai[-1])
    s_listen.listen(1)
    s_ctrl, addr = s_listen.accept()

    # Read client's cookie
    cookie = recvn(s_ctrl, COOKIE_SIZE)
    if DEBUG:
        print(cookie)

    # Ask for parameters
    s_ctrl.sendall(bytes([PARAM_EXCHANGE]))

    # Get parameters
    n = struct.unpack(">I", recvn(s_ctrl, 4))[0]
    param = recvn(s_ctrl, n)
    param = json.loads(str(param, "ascii"))
    if DEBUG:
        print(param)
    reverse = param.get("reverse", False)

    # Ask to create streams
    s_ctrl.sendall(bytes([CREATE_STREAMS]))

    if param.get("tcp", False):
        # Accept stream
        s_data, addr = s_listen.accept()
        print("Accepted connection:", addr)
        recvn(s_data, COOKIE_SIZE)
    elif param.get("udp", False):
        # Close TCP connection and open UDP "connection"
        s_listen.close()
        s_data = socket(ai[0], SOCK_DGRAM)
        s_data.bind(ai[-1])
        data, addr = s_data.recvfrom(4)
        s_data.sendto(b"\x12\x34\x56\x78", addr)
    else:
        assert False

    # Start test
    s_ctrl.sendall(bytes([TEST_START]))

    # Run test
    s_ctrl.sendall(bytes([TEST_RUNNING]))

    # Read data, and wait for client to send TEST_END
    poll = select.poll()
    poll.register(s_ctrl, select.POLLIN)
    if reverse:
        poll.register(s_data, select.POLLOUT)
    else:
        poll.register(s_data, select.POLLIN)
    stats = Stats(param)
    stats.start()
    running = True
    # data_buf = bytearray(urandom(param["len"]))
    data_buf = bytearray(
        urandom(min(1024, param["len"]))
    )  # Reduce buffer size to save memory
    while running:
        for pollable in poll.poll(stats.max_dt_ms()):
            if pollable_is_sock(pollable, s_ctrl):
                cmd = recvn(s_ctrl, 1)[0]
                print(f"received:{cmd}")
                if DEBUG:
                    print(cmd_string.get(cmd, "UNKNOWN_COMMAND"))
                if cmd == TEST_END:
                    running = False
            elif pollable_is_sock(pollable, s_data):
                time.sleep(0.01)  # Add a small delay to prevent overloading
                if reverse:
                    n = s_data.send(data_buf)
                    print(f"sent:{data_buf}")
                    stats.add_bytes(n)
                else:
                    recvninto(s_data, data_buf)
                    stats.add_bytes(len(data_buf))
        stats.update()

    # Need to continue writing so other side doesn't get blocked waiting for data
    if reverse:
        while True:
            for pollable in poll.poll(0):
                if pollable_is_sock(pollable, s_data):
                    s_data.send(data_buf)
                    break
            else:
                break

    stats.stop()

    # Ask to exchange results
    s_ctrl.sendall(bytes([EXCHANGE_RESULTS]))

    # Get client results
    n = struct.unpack(">I", recvn(s_ctrl, 4))[0]
    results = recvn(s_ctrl, n)
    results = json.loads(str(results, "ascii"))
    if DEBUG:
        print(results)

    # Send our results
    results = {
        "cpu_util_total": 1,
        "cpu_util_user": 0.5,
        "cpu_util_system": 0.5,
        "sender_has_retransmits": 1,
        "congestion_used": "cubic",
        "streams": [
            {
                "id": 1,
                "bytes": stats.nb0,
                "retransmits": 0,
                "jitter": 0,
                "errors": 0,
                "packets": stats.np0,
                "start_time": 0,
                "end_time": ticks_diff(stats.t3, stats.t0) * 1e-6,
            }
        ],
    }
    results = json.dumps(results)
    s_ctrl.sendall(struct.pack(">I", len(results)))
    s_ctrl.sendall(bytes(results, "ascii"))

    # Ask to display results
    s_ctrl.sendall(bytes([DISPLAY_RESULTS]))

    # Wait for client to send IPERF_DONE
    cmd = recvn(s_ctrl, 1)[0]
    assert cmd == IPERF_DONE

    # Close all sockets
    s_data.close()
    s_ctrl.close()
    s_listen.close()


def server():
    _delay = 30
    while True:
        try:
            print("Starting server function...")
            server_once()
        except Exception as e:
            print(f"ERROR on running server:{e}({type(e)})")
            from sys import print_exception

            print_exception(e)
            print(f"Waiting {_delay} seconds...")
            time.sleep(_delay)


def main():
    opt_mode = None
    opt_udp = False
    opt_reverse = False

    sys.argv.pop(0)
    while sys.argv:
        opt = sys.argv.pop(0)
        if opt == "-R":
            opt_reverse = True
        elif opt == "-u":
            opt_udp = True
        elif opt == "-s":
            opt_mode = opt
        elif opt == "-c":
            opt_mode = opt
            opt_host = sys.argv.pop(0)
        else:
            print("unknown option:", opt)
            raise SystemExit(1)

    if opt_mode == "-s":
        server()


if sys.platform == "linux":

    def pollable_is_sock(pollable, sock):
        return sock is not None and pollable[0] == sock.fileno()

    def ticks_us():
        return int(time.time() * 1e6)

    def ticks_diff(a, b):
        return a - b

    if __name__ == "__main__":
        main()
else:
    # sys.platform=rp2
    def pollable_is_sock(pollable, sock):
        return pollable[0] == sock

    from time import ticks_us, ticks_diff

    nic = w5x00_init()
    server()
    # _thread.start_new_thread(server, ())
    time.sleep(1)
