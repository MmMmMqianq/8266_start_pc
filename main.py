"""
作者：钱少青
文件名：8266_web_server.py
时间：2021/08/25
"""
import socket
import time
from machine import Pin
import machine
import do_connect


def handle(link, link_address):
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
        response_body = "Relay ON，Start"
        time.sleep(0.5)
        pin14.value(0)
        print(response_body)
    elif request_data.find("shutdown") != -1:
        pin14.value(1)
        response_body = "Relay ON，Shutdown"
        time.sleep(0.5)
        pin14.value(0)
        print(response_body)
    elif request_data.find("res") != -1:
        pin12.value(1)
        response_body = "Relay OFF，Restart"
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


try:
    # 初始化输出引脚，否则输出引脚在上电后会有高电平脉冲式输出
    pin12 = Pin(12, Pin.OUT)
    pin14 = Pin(14, Pin.OUT)
    pin14.value(0)
    pin12.value(0)
    ip_8266 = do_connect.do_connect()
    web_ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    web_ser.bind(('', 80))
    web_ser.listen(5)
    while True:
        print("等待客户端连接...")
        conn, client_address = web_ser.accept()
        handle(conn, client_address)
except OSError:
    machine.reset()
