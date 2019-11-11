# 引入的"simple"头文件放置在同一路径....！！！
from simple import MQTTClient
import network
import time

SERVER = "47.103.121.23"
CLIENT_ID = "L9ZPRGlt6Bl7P8FXYRRd"
TOPIC = "v1/devices/me/telemetry"
username='L9ZPRGlt6Bl7P8FXYRRd'
password=''


def do_connect(essid, password):
    if essid == None or essid == '':
        raise BaseException('essid can not be null')
    if password == None or password == '':
        raise BaseException('password can not be null')
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        print("set sta active")
        sta_if.active(True)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.connect(essid, password)
        retry_times = 30
        while not sta_if.isconnected() and retry_times > 0:
            print(" wait a moment i will try %s items,please" % retry_times)
            time.sleep(2)
            retry_times -= 1
    print('network config:', sta_if.ifconfig())


def disconnect():
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        sta_if.disconnect()
        print('the network had been disconnect')


if __name__ == "__main__":
    essid = 'yuhan888888'
    password = 'yuhan123456'
    messg = "{\"hello\":\"python\"}"
    do_connect(essid, password)
    
    global c  
    server=SERVER
    c = MQTTClient(CLIENT_ID, server,1883,username,password)
    c.connect()
    while 1:
        c.publish(TOPIC,messg,retain= True)
        time.sleep(30)
    
    while True:
        exit = input("press Q to exit:")
        if exit == 'Q':
            disconnect()
            break