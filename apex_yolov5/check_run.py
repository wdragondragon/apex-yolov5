import hashlib
import json
import os
import uuid
from datetime import datetime

import requests
import wmi
from PyQt5.QtWidgets import QMessageBox

s = wmi.WMI()


def get_device_id():
    for item in s.Win32_ComputerSystemProduct():
        return item.UUID


# cpu 序列号
def get_CPU_info():
    cpu = []
    cp = s.Win32_Processor()
    for u in cp:
        cpu.append(
            {
                "Name": u.Name,
                "Serial Number": u.ProcessorId,
                "CoreNum": u.NumberOfCores
            }
        )
    print("cpu info", cpu)
    return cpu


# 硬盘序列号
def get_disk_info():
    disk = []
    for pd in s.Win32_DiskDrive():
        disk.append(
            {
                "Serial": s.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(),  # 获取硬盘序列号，调用另外一个win32 API
                "ID": pd.deviceid,
                "Caption": pd.Caption,
                "size": str(int(float(pd.Size) / 1024 / 1024 / 1024)) + "G"
            }
        )
    return sorted(disk, key=lambda x: x['ID'])


# mac 地址（包括虚拟机的）
def get_network_info():
    network = []
    for nw in s.Win32_NetworkAdapterConfiguration():  # IPEnabled=0
        if nw.MACAddress != None:
            network.append(
                {
                    "MAC": nw.MACAddress,  # 无线局域网适配器 WLAN 物理地址
                    "ip": nw.IPAddress
                }
            )
    return network


# 主板序列号
def get_mainboard_info():
    mainboard = []
    for board_id in s.Win32_BaseBoard():
        mainboard.append(board_id.SerialNumber.strip().strip('.'))
    return mainboard

    # 获取机器码（这里以MAC地址作为机器码）


def get_machine_code():
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i + 2] for i in range(0, 12, 2))


def check_permission(main_windows, machine_code, validate_type):
    # 发送请求到你的验证服务器
    # 你需要替换这个URL为你的服务器地址
    url = "http://1.15.138.227:8123/validate"
    payload = {"machine_code": machine_code, 'validate_type': validate_type}
    response = requests.post(url, data=payload)
    print(response.content.decode('unicode-escape'))
    # 检查服务器的响应
    if response.status_code == 200:
        server_response = response.json()
        if 'access_granted' in server_response:
            # 检查响应中是否包含日期字段
            if 'expiration_time' in server_response:
                # 解析日期字段为 datetime 对象
                expiration_time_str = server_response['expiration_time']
                if expiration_time_str is None:
                    print("欢迎回来：永久授权用户")
                    main_windows.setWindowTitle(main_windows.windowTitle() + " 永久授权")
                else:
                    expiration_time = datetime.strptime(expiration_time_str, "%a, %d %b %Y %H:%M:%S %Z")
                    # 将 expiration_time 格式化为字符串
                    formatted_expiration_time = expiration_time.strftime("%Y-%m-%d %H:%M:%S")

                    print("欢迎回来：授权过期时间：" + formatted_expiration_time)
                    main_windows.setWindowTitle(
                        main_windows.windowTitle() + " 授权过期时间：" + formatted_expiration_time)
            return server_response['access_granted']

    return None


def check(validate_type, main_windows=None):
    main_board_info = get_mainboard_info()
    disk_info = get_disk_info()

    main_board_info_str = json.dumps(main_board_info, sort_keys=True)
    disk_info_str = json.dumps(disk_info, sort_keys=True)

    main_board_info_hash = hashlib.sha256(main_board_info_str.encode()).hexdigest()
    disk_info_hash = hashlib.sha256(disk_info_str.encode()).hexdigest()
    machine_code = hashlib.sha256((main_board_info_hash + "_" + disk_info_hash).encode()).hexdigest()
    print("machine_code:" + machine_code)
    if not check_permission(main_windows, machine_code, validate_type):
        print("没有运行权限")
        QMessageBox.warning(main_windows, "错误", "没有运行权限")
        os._exit(0)
