# 🚀 WIZnet-ioNIC-micropython-examples

- Main firmware repository:
  - [fix-wiznet-timeout](https://github.com/WIZnet-ioNIC/WIZnet-EVB-Pico-micropython/tree/fix-wiznet-timeout) branch **(recommended — required for MQTT)**
  - [WIZnet-ioNIC-micropython](https://github.com/WIZnet-ioNIC/WIZnet-EVB-Pico-micropython/tree/WIZnet-ioNIC-micropython) branch (base PR)
- Upstream MicroPython PR: https://github.com/micropython/micropython/pull/18035
- This repository contains MicroPython example scripts for the WIZnet EVB Boards.

## ⚡ Quick Start (Release UF2 Recommended)

### Step 1: Download Firmware
- Download the appropriate `firmware.uf2` file for your board from the [Releases](https://github.com/WIZnet-ioNIC/WIZnet-EVB-Pico-micropython/releases) page.
    - Example: `build-W55RP20_EVB_PICO/firmware.uf2`, `build-W6300_EVB_PICO/firmware.uf2`

### Step 2: Flash Firmware
1. Hold down the board's **BOOTSEL** button and connect via USB
2. The `RPI-RP2` drive will automatically mount
3. Drag & drop the downloaded **`firmware.uf2`** file into the `RPI-RP2` drive
4. The board will automatically reboot after the copy is complete

> 💡 If you built from source, use `ports/rp2/build-<BOARD>/firmware.uf2` with the same procedure.

---

## 📋 Supported Boards

| Board Series      | Pico                | Pico2               |
|-------------------|---------------------|---------------------|
| **W5100S-EVB**    | W5100S-EVB-Pico     | W5100S-EVB-Pico2    |
| **W5500-EVB**     | W5500-EVB-Pico      | W5500-EVB-Pico2     |
| **W55RP20-EVB**   | W55RP20-EVB-Pico    | -                   |
| **W6100-EVB**     | W6100-EVB-Pico      | W6100-EVB-Pico2     |
| **W6300-EVB**     | W6300-EVB-Pico      | W6300-EVB-Pico2     |

---

## 🛠️ Example Scripts

This repository includes various network example scripts:

- `Loopback.py` : TCP server/client example
- `dhcp.py` : DHCP-based example
- `HTTP_Client.py` : HTTP/HTTPS request examples
- `dns_client.py` : DNS domain name resolution example
- `sntp.py` : NTP time synchronization example
- `redis_client.py` : Redis server connection and data store/retrieve example
- `mqtt_client.py` : MQTT broker subscribe example

Edit the configuration (network, board name, etc.) at the top of each script to match your environment, then run with Thonny or similar tools.

---

## 🧪 Verify Operation (REPL)

After the board reboots, connect to the serial port REPL and test with the following example:

```python
from wiznet_init import wiznet
nic = wiznet("W55RP20-EVB-Pico", dhcp=True)
print('ifconfig:', nic.ifconfig())
```

---

## 🔧 Upload Scripts with Thonny (Optional)

1. In Thonny, set the interpreter to **MicroPython (Raspberry Pi Pico)**
2. After connecting to REPL, upload your example scripts to the board for execution