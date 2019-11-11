from simple import MQTTClient
from machine import Pin
import network
import time


SSID="mimiya20"
PASSWORD="985514185"
led=Pin(14, Pin.OUT, value=0)  #led pin
SERVER = "47.103.121.23"
CLIENT_ID = "XzWGMBcYelr3ceCFmxlD"
TOPIC = b"v1/devices/me/telemetry/sub"
username='XzWGMBcYelr3ceCFmxlD'
password=''
 
def sub_cb(topic, msg):
    global state
    print((topic, msg))
    #tlink.io switch 
    if msg == b"{\"sensorDatas\":[{\"switcher\":1}]}":
            led.value(1)
            #state = 0
            print("1")
    elif msg == b"{\"sensorDatas\":[{\"switcher\":0}]}":
            led.value(0)
            #state = 1
            print("0")
 
def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):

    time.sleep(1)
 
 
def setup():
    global c 
    connectWifi(SSID,PASSWORD)
    server=SERVER
    c = MQTTClient(CLIENT_ID, server,0,username,password)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
 
def main_loop():
    while 1:
        c.wait_msg()
 
def teardown():
    try:
        c.disconnect()
        print("Disconnected.")
    except Exception:
        print("Couldn't disconnect cleanly.")
 
#主程序运行  
if __name__ == '__main__':
  setup() #such as arduino--setup()
  try:
      main_loop() #such as arduino-loop
  finally:
      teardown()