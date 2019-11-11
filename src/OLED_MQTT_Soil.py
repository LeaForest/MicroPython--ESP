from machine import SPI
from machine import Pin
from machine import ADC
from ssd1306 import SSD1306_SPI
from simple import MQTTClient
import network
import time
import json


Wifissid = 'yuhan888888'
Wifipasswd = 'yuhan123456'
SERVER = "47.103.121.23"
CLIENT_ID = "L9ZPRGlt6Bl7P8FXYRRd"
TOPIC = "v1/devices/me/telemetry"
username='L9ZPRGlt6Bl7P8FXYRRd'
passwd=''

# 采用默认的SPI引脚
# spi = SPI(1);
spi = SPI(baudrate=10000000, polarity=1, phase=0, sck=Pin(2,Pin.OUT), mosi=Pin(0,Pin.OUT), miso=Pin(12))
# D0-CLK/sck D1-MOSI 采用自定义的SPI引脚
display = SSD1306_SPI(128, 64, spi, Pin(5), Pin(4), Pin(16));
# 采用自定义的DC  RES  CS 引脚 



def wifi_connect(essid, password):
    if essid == None or essid == '':
        raise BaseException('essid can not be null')
    if password == None or password == '':
        raise BaseException('password can not be null')
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        #print("set sta active")
        sta_if.active(True)
    if not sta_if.isconnected():
        #print('connecting to network...')
        sta_if.connect(essid, password)
        retry_times = 30
        time.sleep(2)
        while not sta_if.isconnected() and retry_times > 0:
            # print(" wait a moment i will try %s items,please" % retry_times)
            time.sleep(2)
            retry_times -= 1
    print('network config:', sta_if.ifconfig())



def soilhum_read():
    adc0=ADC(0)  
    # 数据实时采集:需要进行百分比映射,用以下函数读取干湿情况下的极值
    # valueCheck = ad0.read()
    # 如：“最湿润”时读取的模拟值为：minval = 375;
    #    “最干燥”时读取的模拟值为：maxval = 785;
    maxval = 840
    minval = 375
    soilValue = round(((1024 - adc0.read())- (1024-maxval))/(maxval-minval) * 100,1)
    print(soilValue)
    return(soilValue)



def msg_Pub():
    global c  
    server=SERVER
    c = MQTTClient(CLIENT_ID, server,1883,username,passwd)
    c.connect()
    while True:
      SoilHum = soilhum_read()
      paylod_ = {'SoilHum' : SoilHum }
      msg_ = json.dumps(paylod_)
      c.publish(TOPIC,msg_,retain= True)
      oledisplay(SoilHum)
      time.sleep(2)
      

def oledisplay(SoilHum):
    try:
      # 清屏
      display.fill(0)
      display.invert(0)
      
      display.rect(0,0,128,64,1)
      display.rect(1,1,126,62,1)
      display.hline(1,24,128,1)
      display.hline(15,22,95,1)
      #display.hline(20,18,85,1)
      display.fill_rect(4,27,120,5,1)

      display.text('  SOIL - HUM',4,6)
      display.text('Soilhum :',5,40)
      display.text(str(SoilHum),86,40)
      # 显示内容
      display.show()
      
    except Exception as ex:
      print('Unexpected error: {0}'.format(ex))
      # 关闭显示
      display.poweroff() 



def disconnect():
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        sta_if.disconnect()
        # print('the network had been disconnect')


if __name__ == "__main__":
    display.poweron()
    display.init_display()
   
    wifi_connect(Wifissid, Wifipasswd)
    msg_Pub()