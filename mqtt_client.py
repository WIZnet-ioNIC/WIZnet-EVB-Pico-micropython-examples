# ===== Net Config (edit here) =====
BOARD       = "W6300-EVB-Pico2"  # Board name is case-insensitive
USE_DHCP    = True

# Static IP settings (used when USE_DHCP=False)
NET_IP      = "192.168.11.20"
NET_SN      = "255.255.255.0"
NET_GW      = "192.168.11.1"
NET_DNS     = "8.8.8.8"

MQTT_BROKER = "192.168.11.2"
MQTT_TOPIC  = b"test/topic"
CLIENT_ID   = "wiznet_client"
# ==================================

# NOTE: Run this once before using this script:
#   import mip; mip.install("umqtt.simple")

from umqtt.simple import MQTTClient
from wiznet_init import wiznet

def on_msg(topic, msg):
    print("recv:", topic, msg)

def main():
    if USE_DHCP:
        nic = wiznet(BOARD, dhcp=True)
    else:
        nic = wiznet(BOARD, dhcp=False, ip=NET_IP, sn=NET_SN, gw=NET_GW, dns=NET_DNS)

    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    client.set_callback(on_msg)
    client.connect()
    print("Connected to MQTT broker:", MQTT_BROKER)
    client.subscribe(MQTT_TOPIC)
    print("Subscribed to:", MQTT_TOPIC)

    try:
        while True:
            client.check_msg()
    except OSError as e:
        print("error:", e)
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
