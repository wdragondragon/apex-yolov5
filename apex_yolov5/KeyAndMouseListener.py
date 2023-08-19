import threading

from apex_yolov5.ScreenUtil import select_gun
from apex_yolov5.Tools import Tools
from apex_yolov5.grabscreen import save_screen_to_file
from apex_yolov5.socket.config import global_config


class KeyListener:

    def __init__(self):
        super().__init__()
        self.toggle_key = dict()
        self.refresh_button = global_config.refresh_button

    def on_press(self, key):
        if Tools.is_apex_windows():
            if not hasattr(key, 'name') and hasattr(key, 'char') and key.char is not None:
                # if key.char in self.toggle_key:
                #     self.toggle_key.pop(key.char)
                # else:
                self.toggle_key[key.char] = Tools.current_milli_time()
            elif hasattr(key, 'name') and key.name is not None:
                # if key.name in self.toggle_key:
                #     self.toggle_key.pop(key.name)
                # else:
                self.toggle_key[key.name] = Tools.current_milli_time()

    # 释放按钮，按esc按键会退出监听
    def on_release(self, key):
        if Tools.is_apex_windows():
            if not hasattr(key, 'name') and hasattr(key, 'char') and key.char is not None:
                if key.char in self.toggle_key:
                    self.toggle_key.pop(key.char)
                if key.char in self.refresh_button:
                    threading.Thread(target=select_gun.select_gun).start()
                elif key.char == 'p' or key.char == 'P':
                    threading.Thread(target=save_screen_to_file).start()
            elif hasattr(key, 'name') and key.name is not None:
                if key.name in self.toggle_key:
                    self.toggle_key.pop(key.name)

    def is_open(self, button):
        return button in self.toggle_key


class MouseListener:
    def __init__(self):
        super().__init__()
        self.on_mouse_key_map = dict()
        self.middle_toggle = False

    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.on_mouse_key_map[button] = Tools.current_milli_time()
            if button == button.middle:
                self.middle_toggle = not self.middle_toggle
            # print("左键按下")
        elif not pressed:
            if button not in self.on_mouse_key_map:
                return
            # print("左键释放, 持续时间: {}".format(Tools.current_milli_time() - self.on_mouse_key_map[button]))
            self.on_mouse_key_map.pop(button)

    def on_scroll(self, x, y, dx, dy):
        pass

    def watch_release(self):
        pass

    def is_press(self, button):
        return button in self.on_mouse_key_map

    def press_time(self, button):
        if self.is_press(button):
            return Tools.current_milli_time() - self.on_mouse_key_map[button]
        else:
            return 0


apex_mouse_listener = MouseListener()
apex_key_listener = KeyListener()
