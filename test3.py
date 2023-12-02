import cv2

from apex_yolov5.socket.config import global_config

# camera_id_list = []
# for device in range(0,10000):
#     stream = cv2.VideoCapture(device)
#
#     grabbed = stream.grab()
#     stream.release()
#     if not grabbed:
#         continue
#
#     camera_id_list.append(device)
#
# print(camera_id_list)

# 调用 VideoCapture 参数为0 表示打开笔记本摄像头
# 参数 1 表示打开 usb 摄像头或者加入路径表示打开指定的视屏文件

cap = cv2.VideoCapture(0)  # 视频流
cap.set(cv2.CAP_PROP_FRAME_WIDTH, global_config.desktop_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, global_config.desktop_height)


def get_img_from_cap(monitor):
    ret, frame = cap.read()
    frame = frame[monitor["top"]:monitor["top"] + monitor["height"], monitor["left"]:monitor["left"] + monitor["width"]]
    return frame


# monitor = global_config.monitor
#
# #  isOpened() 表示打开返回 True，失败返回False
# while cap.isOpened():
#     # read() 表示安帧读取返回两个值，ret是布尔值，如果读取帧是正确的则返回True，
#     # 如果文件读取到结尾，它的返回值就为False。
#     # frame就是每一帧的图像，是个三维矩阵。
#     ret, frame = cap.read()
#     print(ret, frame)
#     frame = frame[monitor["top"]:monitor["top"] + monitor["height"], monitor["left"]:monitor["left"] + monitor["width"]]
#     # 显示视屏窗口
#     cv2.imshow('frame', frame)
#     # waitKey(1) 表示等待 1ms 切换到下一帧图像
#     if cv2.waitKey(10) & 0xff == ord('q'):  # 按q退出
#         break
# # 释放视屏
# cap.release()
# # 关闭所有窗口
# cv2.destroyAllWindows()
