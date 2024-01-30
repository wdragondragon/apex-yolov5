import time

from pynput.mouse import Button

from apex_yolov5.mouse_mover.KmBoxNetMover import KmBoxNetMover



class KmBoxNetListener:
    def __init__(self, km_box_net_mover: KmBoxNetMover):
        import kmNet
        self.kmNet = kmNet
        self.km_box_net_mover = km_box_net_mover
        self.listener_sign = False
        self.down_key_map = []
        self.down_mouse_map = []
        kmNet.monitor(10000)

    def km_box_net_start(self):
        self.listener_sign = True
        print("km box net 监听启动")
        from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
        while self.listener_sign:
            if self.kmNet.isdown_left():
                if "left" not in self.down_mouse_map:
                    self.down_mouse_map.append("left")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.left, True)
            else:
                if "left" in self.down_mouse_map:
                    self.down_mouse_map.remove("left")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.left, False)

            if self.kmNet.isdown_right():
                if "right" not in self.down_mouse_map:
                    self.down_mouse_map.append("right")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.right, True)
            else:
                if "right" in self.down_mouse_map:
                    self.down_mouse_map.remove("right")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.right, False)

            if self.kmNet.isdown_middle():
                if "middle" not in self.down_mouse_map:
                    self.down_mouse_map.append("middle")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.middle, True)
            else:
                if "middle" in self.down_mouse_map:
                    self.down_mouse_map.remove("middle")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.middle, False)

            if self.kmNet.isdown_side1():
                if "x1" not in self.down_mouse_map:
                    self.down_mouse_map.append("x1")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x1, True)

            else:
                if "x1" in self.down_mouse_map:
                    self.down_mouse_map.remove("x1")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x1, False)
            if self.kmNet.isdown_side2():
                if "x2" not in self.down_mouse_map:
                    self.down_mouse_map.append("x2")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x2, True)
            else:
                if "x2" in self.down_mouse_map:
                    self.down_mouse_map.remove("x2")
                    apex_mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x2, False)
            time.sleep(0.01)
        print("km box net 监听结束")

    def stop(self):
        self.listener_sign = False
