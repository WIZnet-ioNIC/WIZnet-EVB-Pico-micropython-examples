
<a name="WIZnet-ioNIC-micropyton_README"></a>
WIZnet-ioNIC-micropyton_README
===========================


> The W55RP20 is a System-in-Package (SiP) developed by WIZnet, integrating Raspberry Pi's RP2040 microcontroller, WIZnet's W5500 Ethernet controller, and 2MB of Flash memory into a single chip. These sections will guide you through the steps of configuring a development environment for micropython using the **W55RP20** product from WIZnet.





<a name="hardware_requirements"></a>

# Hardware requirements

| Image                                                                                                                                       | Name                                                                                  | Etc                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| <image src= "https://docs.wiznet.io/assets/images/w55rp20-evb-pico-docs-8e041fe8924bed1c8d567c1c8b87628d.png" width="200px" height="150px"> | [**W55RP20-EVB-PICO**](https://docs.wiznet.io/Product/ioNIC/W55RP20/w55rp20-evb-pico) | [W55RP20 Document](https://docs.wiznet.io/Product/ioNIC/W55RP20/documents_md) |

> ### Pin Diagram

The W55RP20 has internal connections between the RP2040 and W5500 via GPIO pins. The connection table is as follows:

| I/O  | Pin Name | Description                    |
| :--- | -------- | ------------------------------ |
| O    | GPIO20   | Connected to **CSn** on W5500  |
| O    | GPIO21   | Connected to **SCLK** on W5500 |
| I    | GPIO22   | Connected to **MISO** on W5500 |
| O    | GPIO23   | Connected to **MOSI** on W5500 |
| I    | GPIO24   | Connected to **INTn** on W5500 |
| O    | GPIO25   | Connected to **RSTn** on W5500 |


<a name="development_environment_configuration"></a>

# Development environment configuration

<a name="Building"></a>
## Building

1. Clone  
```sh
cd [user path]
git clone https://github.com/WIZnet-ioNIC/WIZnet-ioNIC-micropython.git
git submodule update --init
```

2. Build
```sh
cd WIZnet-ioNIC-micropython/ports/rp2
make BOARD=W55RP20_EVB_PICO
```

3. uf2 file writing  
   Hold down the BOOTSEL button on your W55RP20-EVB-PICO board, press and release the RUN button, and you should see a removable disk pop-up.

```sh
cp build-W55RP20_EVB_PICO/firmware.uf2 /media/[user name]/RPI-RP2
```

4. examples  
   The MicroPython examples for the W55RP20-EVB-PICO can be found at the following path. Please refer to this for guidance.  
```sh
WIZnet-ioNIC-micropython/WIZnet-ioNIC_examples
```

The pre-built bin files (WIZnet-ioNIC-micropython_Bin.zip) can be found at the following path:  
https://github.com/WIZnet-ioNIC/WIZnet-ioNIC-micropython/releases  

For the guide document that includes the video, please refer to the link below.
https://maker.wiznet.io/mason/projects/how%2Dto%2Dbuild%2Dwiznet%2Dionic%2Dmicropython/


# W55RP20 Micropython Examples


## Loopback

**File:** `Loopback.py`

In the main function, uncomment the server_loop() call to activate server mode on the W55RP20 board.

```python
def main():
    w5x00_init()  # Initialize network

    ###TCP SERVER###
    server_loop()  # Enable server function (uncomment this line)

    ###TCP CLIENT###
    #client_loop()  # Client function (comment this line)
```

Use the following network settings:

IP: 192.168.11.20

Port: 5000

Testing Client

Use another device on the same network to connect as a TCP client to the server.


### Using Python to Connect as a Client:
```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.11.20', 5000))

s.sendall(b'Hello, Server!')
data = s.recv(1024)
print('Received', data.decode('utf-8'))

s.close()
```

## Loopback dhcp server

**File:** `Loopback_dhcp.py`

The functionality is the same as the loopback setup. The only difference is that this version uses DHCP to automatically get the IP address.

**File:** `HTTP_Client.py`

This code uses the WIZnet W5x00 series Ethernet chip (specifically W55RP20) to connect to a network and send HTTP GET and POST requests. Using the urequests module, the code sends HTTP requests and prints the responses, verifying that the network communication is working correctly.

### HTTP Request (request function):
Sends a GET request to http://httpbin.org/get, printing the status code and response content.
Then sends a POST request to http://httpbin.org/post with some JSON data, and prints the result as JSON.
Expected Output:

The response status code (200 OK) and response content from the GET request are printed.
The JSON response from the POST request is also printed.

### Static IP as Default
By default, the code uses a static IP address 192.168.11.20.
The network settings are defined as follows:

```python
nic.ifconfig(('192.168.11.20', '255.255.255.0', '192.168.11.1', '8.8.8.8'))
```

### How to Use Dynamic IP
To use a dynamic IP (DHCP), modify the settings as follows:

```python
#None DHCP
# nic.ifconfig(('192.168.11.20','255.255.255.0','192.168.11.1','8.8.8.8'))

#DHCP
nic.ifconfig('dhcp')
```

## SNTP Client

**File:** sntp.py

This code demonstrates how to initialize a WIZnet W5x00 series Ethernet chip to connect to a network and synchronize time with an SNTP server. The example supports both static and dynamic IP configurations, allowing the device to send an SNTP request to an NTP server and print the received time in UTC.

### Expected Output

```shell
Setting up UDP socket...
Creating SNTP request packet...
Resolving NTP server address...
Sending NTP request to pool.ntp.org (192.168.x.x)
Waiting for SNTP response...
SNTP response received!
NTP Time (UTC): (2024, 11, 25, 10, 30, 45, 0, 329)
Attempt 1 failed, retrying in 1 second(s)...(Exception details)
NTP request timed out.
```

If there are any connection issues, you may see messages like:

```shell
Attempt 1 failed, retrying in 1 second(s)...(Exception details)
NTP request timed out.
```

### Important Considerations

For IP settings, refer to previous examples for how to configure static or dynamic IP addresses.

## Redis Client

**File:** `redis_client.py`

**Dependency:** `picoredis.py`

When run on the W55RP20 through Thonny, this script connects to a Redis server and performs a few operations:

1. **Ping Command**: Sends an empty `ping` request and another with the string "os" to the Redis server. The server responds with `PONG` and `os` respectively.
2. **Set Command**: Creates a key named `pico` with the value `test from pico` on the Redis server.
3. **Get Command**: Retrieves the value of the `pico` key from the Redis server and prints it, verifying that the key was properly stored.

For more details on available Redis commands, please visit the official documentation: [Redis Commands](https://redis.io/docs/latest/commands/).

## iPerf Server for W55RP20-EVB-Pico

**File:** `iperf3.py`

When executed as a server process, this script performs the following actions:

1. Obtains an IP address via DHCP
2. Opens and listens on port 5201

### Performance Note

Due to the nature of MicroPython execution, the test results may show lower performance compared to the board's actual capabilities. This is an inherent limitation of the interpreted language environment.

### Recommendation for Accurate Performance Testing

For more accurate iPerf test results that reflect the true performance of the W55RP20-EVB-Pico board, we recommend using the C language implementation.

Please refer to the following repository for a C-based iPerf implementation:

[WIZnet-PICO-IPERF-C](https://github.com/WIZnet-ioNIC/WIZnet-PICO-IPERF-C/)

This C implementation will provide more representative performance metrics for the W55RP20-EVB-Pico board.



## Windows iPerf3 Test Script for W55RP20

 **File:** `iperf3_test.py`

This script is designed to test the `iperf3.py` running on the W55RP20 board from a Windows environment.

### Purpose

The primary purpose of this script is to facilitate iPerf3 testing between a Windows machine and a W55RP20 board running the `iperf3.py` script.

### Usage Instructions

To use this script, follow these steps:

1. Ensure the `iperf3.py` script is running on your W55RP20 board.
2. Note the IP address displayed by the W55RP20 board.
3. Open a command prompt or PowerShell window on your Windows machine.
4. Navigate to the directory containing this script.
5. Run the script using the following command format:

