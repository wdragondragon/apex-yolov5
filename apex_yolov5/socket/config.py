import pynput
import torch


# listener_ip = '192.168.10.3'
listener_ip = 'localhost'
listener_port = 8888
buffer_size = 4096

device = 'cuda' if torch.cuda.is_available() else 'cpu'
# device = 'cpu'
half = device != 'cpu'
imgsz = 640
conf_thres = 0.5
iou_thres = 0.05
# screen_width, screen_height = (1920, 1080)  # 1280 * 1024
screen_width, screen_height = (2560, 1440)
# 截屏区域
# offet_Shot_Screen = 30  # 屏幕截图偏移量,
offet_Shot_Screen = 20  # 屏幕截图偏移量,
# 默认16：9, 1920x1080 , 960, 540是屏幕中心，根据自己的屏幕修改
left_top_x = screen_width // 2 - offet_Shot_Screen * 16
left_top_y = screen_height // 2 - offet_Shot_Screen * 9
right_bottom_x = screen_width // 2 + offet_Shot_Screen * 16
right_bottom_y = screen_height // 2 + offet_Shot_Screen * 9
shot_width = 2 * offet_Shot_Screen * 16  # 截屏区域的实际大小需要乘以2，因为是计算的中心点
shot_height = 2 * offet_Shot_Screen * 9
region = (left_top_x, left_top_y, right_bottom_x, right_bottom_y)

window_name = "test"
auto = True

mouse = pynput.mouse.Controller()  # 鼠标对象
lock_button = "left"  # 无用，apex为按住鼠标左或者右其中一个为就为lock模式，建议在游戏设置按住开镜
is_show_debug_window = True  # 可修改为True，会出现调试窗口
