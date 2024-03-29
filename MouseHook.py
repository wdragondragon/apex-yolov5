# import os.path as op
# import json
# import threading
# import time
#
# import pynput
# from pynput.mouse import Button
#
# from apex_yolov5 import auxiliary
# from apex_yolov5.KeyAndMouseListener import apex_mouse_listener
# from apex_yolov5.auxiliary import set_intention
#
#
# class MouseHook:
#     def __init__(self):
#         config_file_path = 'specs.json'
#         if op.exists(config_file_path):
#             with open(config_file_path) as file:
#                 self.specs_data = json.load(file)
#                 print("加载配置文件: {}".format(config_file_path))
#         else:
#             print("配置文件不存在: {}".format(config_file_path))
#
#     def get_config(self, name):
#         for spec in self.specs_data:
#             if spec['name'] == name:
#                 return spec
#         return None
#
#
# listener = pynput.mouse.Listener(
#     on_click=apex_mouse_listener.on_click)
# listener.start()
# threading.Thread(target=auxiliary.start).start()
# mouse_hook = MouseHook()
# spec = mouse_hook.get_config("car")
# print(spec)
#
# start_time = None
# pre_x, pre_y = 0, 0
# i = 0
# while True:
#     if apex_mouse_listener.is_press(Button.left) and apex_mouse_listener.is_press(Button.right):
#         if start_time is None:
#             start_time = time.time()
#         index = next(
#             (i for i, time_point in enumerate(spec['time_points']) if time_point >= (time.time() - start_time) * 1000),
#             None)
#         if index is not None and i < index:
#             print(str(index))
#             # 获取对应下标的x和y
#             x_value = spec['x'][index] - pre_x
#             y_value = spec['y'][index] - pre_y
#             set_intention(-x_value, -y_value, 0, 0)
#             pre_x, pre_y = x_value, y_value
#             i = index
#     else:
#         start_time = None
#         pre_x, pre_y, i = 0, 0, 0
#     time.sleep(0.001)
