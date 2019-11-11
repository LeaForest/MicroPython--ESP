import network
import time


def do_connect(essid, password):
    '''
    根据给定的eddid和password连接wifi
    :param essid:  wifi sid
    :param password:  password
    :return:  None
    '''
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
    '''
    断开网络连接
    :return:  None
    '''
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        sta_if.disconnect()
        print('the network had been disconnect')


if __name__ == "__main__":
    essid = 'mimiya20'
    password = '985514185'
    do_connect(essid, password)
    while True:
        exit = input("press Q to exit:")
        if exit == 'Q':
            disconnect()
            break
