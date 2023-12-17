from ctypes import CDLL

gmok = False
gm = None


# try:
#     gm = CDLL(r'./ghub_device1.dll')
#     gmok = gm.device_open() == 1
#     if not gmok:
#         print('未安装ghub或者lgs驱动!!!')
#     else:
#         print('初始化成功!')
# except FileNotFoundError:
#     print('缺少文件')


# 按下鼠标按键
def press_mouse_button(button):
    if gmok:
        gm.mouse_down(button)


# 松开鼠标按键
def release_mouse_button(button):
    if gmok:
        gm.mouse_up(button)


# 点击鼠标
def click_mouse_button(button):
    press_mouse_button(button)
    release_mouse_button(button)


# 按下键盘按键
def press_key(code):
    if gmok:
        gm.key_down(code)


# 松开键盘按键
def release_key(code):
    if gmok:
        gm.key_up(code)


# 点击键盘按键
def click_key(code):
    press_key(code)
    release_key(code)


# 鼠标移动
def mouse_xy(x, y, abs_move=False):
    if gmok:
        gm.moveR(int(x), int(y), abs_move)
