import socket
import time
from w5x00 import w5x00_init  # Initialize WIZnet W5x00 Ethernet module

# Target server IP and port settings
destip = "192.168.7.3"
destport = 2300
conn_info = (destip, destport)  # Store (IP, port) as a tuple

conn_flag = False  # Connection status flag


def client_loop(ip):
    """
    TCP client loop: Continuously attempts to connect to the server
    and handles data transmission upon successful connection.
    """
    print(f"my ip is {ip}")  # Print the device's IP address
    global conn_flag
    s = None  # Initialize the socket object

    while True:
        t_begin = time.time()  # Record loop start time

        # Attempt to connect if not already connected
        while not conn_flag:
            try:
                if not s:
                    s = socket.socket()  # Create a socket object
                s.connect(conn_info)  # Attempt to connect to the server
                conn_flag = True  # Set flag on successful connection
                print(f"Loopback client Connect! ({time.time() - t_begin}) seconds")
            except Exception as e:
                # Print error message if connection fails
                print("connect error\r\n", e, f" ({time.time() - t_begin}) seconds")
                conn_flag = False  # Reset connection flag
                s.close()  # Close socket
                s = None  # Delete socket object
                time.sleep(2)  # Retry after 2 seconds

        try:
            data = s.recv(2048)  # Receive data from server (max 2048 bytes)
            data = data.decode("utf-8")  # Convert to UTF-8 string

            if data != "NULL":  # Process only if data is not "NULL"
                # Print received data
                print(
                    "recv from {0}:[{1}]: {2}\r\n".format(
                        conn_info[0], conn_info[1], data
                    ),
                    f" ({time.time() - t_begin}) seconds",
                )
                s.send(data)  # Echo received data back to the server
        except Exception as e:
            # Print error message if the connection is lost
            print("disconnect", e, f" ({time.time() - t_begin}) seconds")
            conn_flag = False  # Reset connection flag


def main():
    """
    Main function: Initializes the W5x00 Ethernet module and starts the client loop.
    """
    ip = w5x00_init()  # Initialize the Ethernet module and obtain an IP address
    client_loop(ip.ifconfig()[0])  # Start the client loop


if __name__ == "__main__":
    main()  # Run the program
