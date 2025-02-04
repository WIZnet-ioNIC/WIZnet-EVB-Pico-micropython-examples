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
keepalive = 60

last_message = 0
message_interval = 5
counter = 0


def sub_callback(topic, msg):
    print("received data: ", (topic, msg))


def mqtt_connect(client_id, mqtt_server, port, keepalive=60):
    client = MQTTClient(client_id, mqtt_server, port=port, keepalive=keepalive)
    client.set_callback(sub_callback)
    client.connect()
    print("Connected to %s MQTT Broker" % (mqtt_server))
    return client


# reconnect & reset
def reconnect(delay=5):
    print("Failed to connected to MQTT Broker. Reconnecting...")
    time.sleep(delay)
    machine.reset()


def main(qos=1, delay=2):
    w5x00_init()

    t_begin = time.time()
    try:
        client = mqtt_connect(client_id, mqtt_server, port, keepalive)
        client.subscribe(topic_pub)
    except OSError:
        reconnect(message_interval)
    except Exception as e:
        print(f"ERROR: on mqtt_connect: {e}")

    i = 0
    while True:
        try:
            print(i, "th try")
            new_data = topic_msg + str(i).encode()
            client.publish(topic_pub, new_data, qos=qos)
            # client.publish(topic_pub, new_data)
            print(f"new data(qos={qos}): ({new_data}) is published!!")
            i += 1
            time.sleep(message_interval)
            client.wait_msg()
        except Exception as e:
            print(f"ERROR: inner while: {e} during {time.time() - t_begin} seconds")
            time.sleep(message_interval)
            break
    client.disconnect()


if __name__ == "__main__":
    while True:
        try:
            print("running main")
            main()
        except Exception as e:
            print(f"ERROR: outer while: {e}")
