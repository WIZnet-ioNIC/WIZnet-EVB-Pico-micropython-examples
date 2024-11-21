from usocket import socket
from machine import Pin,WIZNET_PIO_SPI
import network
import time

def w5x00_init():
    spi = WIZNET_PIO_SPI(baudrate=31_250_000, mosi=Pin(23),miso=Pin(22),sck=Pin(21)) #W55RP20 PIO_SPI
    nic = network.WIZNET5K(spi,Pin(20),Pin(25)) #spi,cs,reset pin
    nic.active(True)
# If you use the Dynamic IP(DHCP), you must use the "nic.ifconfig('dhcp')".
    nic.ifconfig('dhcp')
# If you use the Static IP, you must use the  "nic.ifconfig("IP","subnet","Gateway","DNS")".
    #nic.ifconfig(('192.168.100.13','255.255.255.0','192.168.100.1','8.8.8.8'))
       
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
        
def main():
    w5x00_init()
    
if __name__ == "__main__":
    main()
