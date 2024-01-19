import threading
import time

from pynput.mouse import Button

from apex_yolov5.ScreenUtil import select_gun
from apex_yolov5.Tools import Tools
from apex_yolov5.grabscreen import save_screen_to_file
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket.config import global_config


class KeyListener:

    def __init__(self):
        super().__init__()
        self.press_key = dict()
        self.refresh_button = global_config.refresh_button
        self.toggle_key_map = []

    def on_press(self, key):
        key_name = None
        if not hasattr(key, 'name') and hasattr(key, 'char') and key.char is not None:
            self.press_key[key.char] = Tools.current_milli_time()
            key_name = key.char
        elif hasattr(key, 'name') and key.name is not None:
            self.press_key[key.name] = Tools.current_milli_time()
            key_name = key.name

        if key_name in self.toggle_key_map:
            self.toggle_key_map.remove(key_name)
        else:
            self.toggle_key_map.append(key_name)
        for cb in KMCallBack.toggle_call_back:
            if cb.type == 'k' and cb.key == key_name:
                cb.call_back(True, cb.key in self.toggle_key_map)

    # 释放按钮，按esc按键会退出监听
    def on_release(self, key):
        if not hasattr(key, 'name') and hasattr(key, 'char') and key.char is not None:
            if key.char in self.press_key:
                self.press_key.pop(key.char)
            if key.char in self.refresh_button:
                threading.Thread(target=select_gun.select_gun).start()
            elif key.char == 'p' or key.char == 'P':
                threading.Thread(target=save_screen_to_file).start()
        elif hasattr(key, 'name') and key.name is not None:
            if key.name in self.press_key:
                self.press_key.pop(key.name)

    def is_open(self, button):
        return button in self.press_key


class MouseListener:
    def __init__(self):
        super().__init__()
        self.on_mouse_key_map = dict()
        self.toggle_mouse_key_map = []
        self.move_metering = None

    def on_move(self, x, y):
        if MoverFactory.mouse_mover() is None:
            return
        if self.move_metering is None:
            self.move_metering = (time.time(), (MoverFactory.mouse_mover().get_position()), 0, 0)
        pre_time, (pre_x, pre_y), metering_x, metering_y = self.move_metering
        now = time.time()
        if int((now - pre_time) * 1000) < 500:
            self.move_metering = (pre_time, (x, y), metering_x + abs(pre_x - x), metering_y + abs(pre_y - y))
        else:
            # print(f"1秒鼠标移动幅度：[{metering_x, metering_y}]")
            self.move_metering = (time.time(), (x, y), abs(pre_x - x), abs(pre_y - y))

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.on_mouse_key_map[button] = Tools.current_milli_time()
            if button.name in self.toggle_mouse_key_map:
                self.toggle_mouse_key_map.remove(button.name)
            else:
                self.toggle_mouse_key_map.append(button.name)
            for cb in KMCallBack.toggle_call_back:
                if cb.type == 'm' and cb.key == button.name and cb.is_press:
                    cb.call_back(pressed, cb.key in self.toggle_mouse_key_map)
            # print("左键按下")
        elif not pressed:
            if button not in self.on_mouse_key_map:
                return
            # print("左键释放, 持续时间: {}".format(Tools.current_milli_time() - self.on_mouse_key_map[button]))
            self.on_mouse_key_map.pop(button)
            for cb in KMCallBack.toggle_call_back:
                if cb.type == 'm' and cb.key == button.name and not cb.is_press:
                    cb.call_back(pressed, cb.key in self.toggle_mouse_key_map)

    def on_scroll(self, x, y, dx, dy):
        pass

    def watch_release(self):
        pass

    def is_press(self, button):
        return button in self.on_mouse_key_map

    def is_toggle(self, button):
        return button.name in self.toggle_mouse_key_map

    def press_time(self, button):
        if self.is_press(button):
            return Tools.current_milli_time() - self.on_mouse_key_map[button]
        else:
            return 0

    def get_aim_status(self):
        if global_config.aim_model == "按住":
            return self.is_press(Button.right)
        elif global_config.aim_model == "切换":
            return self.is_toggle(Button.right)


class KMCallBack:
    toggle_call_back = []

    def __init__(self, type, key, call_back, is_press=True):
        super().__init__()
        self.type = type
        self.key = key
        self.call_back = call_back
        self.is_press = is_press

    @staticmethod
    def connect(callback):
        KMCallBack.toggle_call_back.append(callback)

    @staticmethod
    def remove(type, key):
        remove_cb = []
        for cb in KMCallBack.toggle_call_back:
            if cb.type == type and cb.key == key:
                remove_cb.append(cb)
        for cb in remove_cb:
            KMCallBack.toggle_call_back.remove(cb)


apex_mouse_listener = MouseListener()
apex_key_listener = KeyListener()
