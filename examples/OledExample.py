# 适用于实验室现存的0.96“和1.32”OLED，可进行SPI、IIC引脚的自定义设置
from micropython import const
from machine import SPI
from machine import Pin
#from pyb import Pin
from ssd1306 import SSD1306_SPI
import time
import math

#i2c = I2C(scl=Pin(14), sda=Pin(2), freq=100000)
#display = ssd1306.SSD1306_I2C(128,64, i2c)
# IIC引脚连接OLED

# spi = SPI(1);# 采用默认的SPI引脚
spi = SPI(baudrate=10000000, polarity=1, phase=0, sck=Pin(2,Pin.OUT), mosi=Pin(0,Pin.OUT), miso=Pin(12))
# D0-CLK/sck D1-MOSI 采用自定义的SPI引脚
display = SSD1306_SPI(128, 64, spi, Pin(5), Pin(4), Pin(16));
# 采用自定义的DC  RES  CS 引脚 

try:
  display.poweron()
  display.init_display()

  display.text('ESP-mp SPI OLED',1,1)
  display.text('Hi, MicroPython!',1,16)
  display.text('By: hbzjt2012',1,31)
  
  # Write display buffer
  display.show()
  time.sleep(3)

  display.fill(0)
  for x in range(0, 128):
    display.pixel(x, 32+int(math.sin(x/64*math.pi)*7 + 8), 1)
  display.show()
  time.sleep(3)

  display.fill(0)

  x = 0
  y = 0
  direction_x = True
  direction_y = True

  while True:
    # Clear the previous lines
    prev_x = x
    prev_y = y

    # Move bars
    x += (1 if direction_x else -1)
    y += (1 if direction_y else -1)

    # Bounce back, if required
    if x == 128:
       direction_x = False
       x = 126
    elif x == -1:
       direction_x = True
       x = 1
    if y == 64:
       direction_y = False
       y = 63
    elif y == -1:
       direction_y = True
       y = 1

    # Draw new lines
    for i in range(64):
      display.pixel(prev_x, i, False)
      display.pixel(x, i, True)
    for i in range(128):
      display.pixel(i, prev_y, False)
      display.pixel(i, y, True)

    # Make sure the corners are active
    display.pixel(0,   0,  True)
    display.pixel(127, 0,  True)
    display.pixel(0,   63, True)
    display.pixel(127, 63, True)
   
    # Write display buffer
    display.show()


except Exception as ex:
  print('Unexpected error: {0}'.format(ex))
  display.poweroff()