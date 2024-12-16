from umqttsimple import MQTTClient
from usocket import socket
from machine import Pin, SPI
import network
import time
from w5x00 import w5x00_init

# mqtt config
mqtt_server = "192.168.1.2"
port = 1883
client_id = "wiz2"
topic_pub = b"kkk"
topic_msg = b"Hello Pico"

last_message = 0
message_interval = 5
counter = 0


def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port=port, keepalive=60)
    client.connect()
    print("Connected to %s MQTT Broker" % (mqtt_server))
    return client


# reconnect & reset
def reconnect():
    print("Failed to connected to MQTT Broker. Reconnecting...")
    time.sleep(5)
    machine.reset()


def main():
    w5x00_init()

    # try:
    #    client = mqtt_connect()
    # except OSError as e:
    #    reconnect()
    # except Exception as e:
    #    print(f"ERROR: on mqtt_connect: {e}")
    client = mqtt_connect()

    while True:
        client.publish(topic_pub, topic_msg)
        time.sleep(3)
    client.disconnect()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"ERROR: {e}")
