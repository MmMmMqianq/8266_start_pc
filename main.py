






"""
作者：钱少青
文件名：8266_web_server.py
时间：2021/08/25
"""
import socket
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import machine
import do_connect


def handle(link, link_address, ip_8266):
    """处理客户端请求"""
    print("客户端的IP: %s，端口号: %d" % (link_address[0], link_address[1]))
    # 接收客户端请求
    request_data = link.recv(1024).decode()
    print("request data: ", request_data)

    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_server = "Server: QSQSQSQ\r\n"
    response_body_start = "\r\n"

    # 执行动作
    if request_data.find("start") != -1:
        pin14.value(1)
        response_body = "Relay ON, Start"

        response_show = "PC started"
        time.sleep(0.5)
        pin14.value(0)
        print(response_body)
    elif request_data.find("shutdown") != -1:
        pin14.value(1)
        response_body = "Relay ON，Shutdown"
        response_show = "PC shutdowm"
        time.sleep(0.5)
        pin14.value(0)
        print(response_body)
    elif request_data.find("res") != -1:
        pin12.value(1)
        response_body = "Relay OFF，Restart"
        response_show = "PC restart"
        time.sleep(0.5)
        pin12.value(0)
        print(response_body)
    else:
        response_body = "操作不正确！"
        response_start_line = "HTTP/1.1 400 NOT FOUND\r\n"
        print(response_body)

    response = (response_start_line + response_server + response_body_start + response_body).encode()

    # 发送响应数据
    link.sendall(response)

    # 关闭子进程连接
    link.close()
    print("*" * 20)
    oled.fill(0)
    oled.text("8266 IP address:", 0, 0)
    oled.text(ip_8266[0], 0, 8)
    oled.text("client IP addr:", 0, 24)
    oled.text(link_address[0], 0, 32)
    oled.text(response_show, 0, 40)
    oled.text("waiting for connect...", 0, 54)
    oled.show()


try:
    # 初始化输出引脚，否则输出引脚在上电后会有高电平脉冲式输出
    pin12 = Pin(12, Pin.OUT)
    pin14 = Pin(14, Pin.OUT)
    pin14.value(0)
    pin12.value(0)
    ip_8266 = do_connect.do_connect()
    print(ip_8266[0])
    
    i2c = I2C(sda= Pin(4), scl=Pin(5), freq=400000)
    print(i2c.scan())
    oled = SSD1306_I2C(128, 64, i2c)
    oled.contrast(255)  # 调节亮度0-255
    oled.fill(0)
    oled.text("8266 IP address:", 0, 0)
    oled.text(ip_8266[0], 0, 8)
    oled.show()
    
    web_ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    web_ser.bind(('', 80))
    web_ser.listen(5)
    oled.text("waiting for connect...", 0, 24)
    oled.show()
    while True:
        print("等待客户端连接...")
        conn, client_address = web_ser.accept()
        handle(conn, client_address, ip_8266)
except OSError:
    machine.reset()









