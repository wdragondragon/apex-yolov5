import uuid
import os
import requests
import sys
import uuid


# 获取机器码（这里以MAC地址作为机器码）
def get_machine_code():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i + 2] for i in range(0, 12, 2))


def check_permission(machine_code):
    # 发送请求到你的验证服务器
    # 你需要替换这个URL为你的服务器地址
    url = "http://1.15.138.227:8123/validate"
    payload = {"machine_code": machine_code}
    response = requests.post(url, data=payload)
    print(response)
    # 检查服务器的响应
    if response.status_code == 200:
        server_response = response.json()
        if 'access_granted' in server_response:
            return server_response['access_granted']

    return False


def check():
    machine_code = get_machine_code()

    if not check_permission(machine_code):
        print("没有运行权限")
        sys.exit(1)

    # 你的程序的主要部分在这里开始
    print("开始运行程序...")
