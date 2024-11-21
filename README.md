
<a name="WIZnet-ioNIC-micropyton_README"></a>
WIZnet-ioNIC-micropyton_README
===========================


> The W55RP20 is a System-in-Package (SiP) developed by WIZnet, integrating Raspberry Pi's RP2040 microcontroller, WIZnet's W5500 Ethernet controller, and 2MB of Flash memory into a single chip. These sections will guide you through the steps of configuring a development environment for micropython using the **W55RP20** product from WIZnet.





<a name="hardware_requirements"></a>

# Hardware requirements

| Image                                                        | Name                                                      | Etc                                                          |
| ------------------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------ |
| <image src= "https://docs.wiznet.io/assets/images/w55rp20-evb-pico-docs-8e041fe8924bed1c8d567c1c8b87628d.png" width="200px" height="150px"> | [**W55RP20-EVB-PICO**](https://docs.wiznet.io/Product/ioNIC/W55RP20/w55rp20-evb-pico)           | [W55RP20 Document](https://docs.wiznet.io/Product/ioNIC/W55RP20/documents_md) |

> ### Pin Diagram

The W55RP20 has internal connections between the RP2040 and W5500 via GPIO pins. The connection table is as follows:

| I/O  | Pin Name | Description                                    |
| :--- | -------- | ---------------------------------------------- |
| O    | GPIO20   | Connected to **CSn** on W5500                  |
| O    | GPIO21   | Connected to **SCLK** on W5500                 |
| I    | GPIO22   | Connected to **MISO** on W5500                 |
| O    | GPIO23   | Connected to **MOSI** on W5500                 |
| I    | GPIO24   | Connected to **INTn** on W5500                 |
| O    | GPIO25   | Connected to **RSTn** on W5500                 |


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

## SNTP Client

**File:** `sntp.py`

This script retrieves the current time by running on the W55RP20 device through Thonny.

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

