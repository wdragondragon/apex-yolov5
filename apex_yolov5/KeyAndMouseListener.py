import time

from pynput.mouse import Button

from apex_yolov5.Tools import Tools
from apex_yolov5.mouse_mover import MoverFactory
from apex_yolov5.socket.config import global_config


class KeyListener:

    def __init__(self):
        super().__init__()
        self.press_key = dict()
        self.refresh_button = global_config.refresh_button
        self.toggle_key_map = []

    def on_press(self, key):
        """
            键盘按下事件
        :param key:
        """
        key_name = self.get_key_name(key)

        if key_name is not None:
            self.press_key[key_name] = Tools.current_milli_time()

        if key_name in self.toggle_key_map:
            self.toggle_key_map.remove(key_name)
        else:
            self.toggle_key_map.append(key_name)
        for cb in KMCallBack.toggle_call_back:
            if cb.key_type == 'k' and cb.key == key_name and cb.is_press:
                cb.call_back(True, cb.key in self.toggle_key_map)

    # 释放按钮，按esc按键会退出监听
    def on_release(self, key):
        """
            键盘释放事件
        :param key:
        """
        key_name = self.get_key_name(key)
        if key_name is not None and key_name in self.press_key:
            self.press_key.pop(key_name)
        for cb in KMCallBack.toggle_call_back:
            if cb.key_type == 'k' and cb.key == key_name and not cb.is_press:
                cb.call_back(True, cb.key in self.toggle_key_map)

    def is_open(self, button):
        """
            判断按钮作为开关的开关状态
        :param button:
        :return:
        """
        return button in self.press_key

    def get_key_name(self, key):
        """
            从key中获取key_name
        :param key:
        :return:
        """
        key_name = None
        if not hasattr(key, 'name') and hasattr(key, 'char') and key.char is not None:
            key_name = key.char
        elif hasattr(key, 'name') and key.name is not None:
            key_name = key.name
        return key_name


class MouseListener:
    def __init__(self):
        super().__init__()
        self.on_mouse_key_map = dict()
        self.toggle_mouse_key_map = []
        self.move_metering = None
        self.move_avg_x = 1
        self.move_avg_y = 1

    def on_move(self, x, y):
        if MoverFactory.mouse_mover() is None:
            return
        if self.move_metering is None:
            self.move_metering = (time.time(), (MoverFactory.mouse_mover().get_position()), 0, 0, 0, 0)
        pre_time, (pre_x, pre_y), metering_x, metering_y, move_time_x, move_time_y = self.move_metering
        now = time.time()
        abs_x = abs(pre_x - x)
        abs_y = abs(pre_y - y)
        if int((now - pre_time) * 1000) < 100:
            if abs_x > 0:
                move_time_x += 1
            if abs_y > 0:
                move_time_y += 1
            self.move_metering = (
                pre_time, (x, y), metering_x + abs_x, metering_y + abs_y, move_time_x, move_time_y)
        else:
            avg_x = 0 if move_time_x == 0 else metering_x / move_time_x
            avg_y = 0 if move_time_y == 0 else metering_y / move_time_y
            # print(
            #     f"1秒鼠标移动幅度：[{metering_x, metering_y}],移动次数：[{move_time_x, move_time_y}]，平均每次：[{avg_x, avg_y}]")
            self.move_metering = (time.time(), (x, y), abs_x, abs_y, 1 if abs_x > 0 else 0, 1 if abs_y > 0 else 0)
            self.move_avg_x = max(1, round(avg_x, 0))
            self.move_avg_y = max(1, round(avg_y, 0))

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button in self.on_mouse_key_map:
                return
            self.on_mouse_key_map[button] = Tools.current_milli_time()
            if button.name in self.toggle_mouse_key_map:
                self.toggle_mouse_key_map.remove(button.name)
            else:
                self.toggle_mouse_key_map.append(button.name)
            for cb in KMCallBack.toggle_call_back:
                if cb.key_type == 'm' and cb.key == button.name and cb.is_press:
                    cb.call_back(pressed, cb.key in self.toggle_mouse_key_map)
            # print("左键按下")
        elif not pressed:
            if button not in self.on_mouse_key_map:
                return
            # print("左键释放, 持续时间: {}".format(Tools.current_milli_time() - self.on_mouse_key_map[button]))
            self.on_mouse_key_map.pop(button)
            for cb in KMCallBack.toggle_call_back:
                if cb.key_type == 'm' and cb.key == button.name and not cb.is_press:
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
    """
        注册键盘或鼠标回调事件
    """
    toggle_call_back = []

    def __init__(self, key_type, key, call_back, is_press=True):
        super().__init__()
        self.key_type = key_type
        self.key = key
        self.call_back = call_back
        self.is_press = is_press

    @staticmethod
    def connect(callback):
        """
            注册事件
        :param callback:
        """
        KMCallBack.toggle_call_back.append(callback)

    @staticmethod
    def remove(key_type, key, is_press=True):
        """
            移除事件
        :param key_type:
        :param key:
        :param is_press:
        """
        remove_cb = []
        for cb in KMCallBack.toggle_call_back:
            if cb.key_type == key_type and cb.key == key and cb.is_press == is_press:
                remove_cb.append(cb)
        for cb in remove_cb:
            KMCallBack.toggle_call_back.remove(cb)


apex_mouse_listener = MouseListener()
apex_key_listener = KeyListener()
