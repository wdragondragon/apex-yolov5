import cv2

from apex_yolov5.log.Logger import Logger


class CapScreenTaker:
    """
        本地截图
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        self.cap = cv2.VideoCapture(0)  # 视频流
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.logger.print_log("使用视频采集卡")

    def get_images_from_bbox(self, bbox_list):
        frames = []
        ret, frame = self.cap.read()
        for monitor in bbox_list:
            frames.append(frame[monitor[1]: monitor[3], monitor[0]: monitor[2]])
        return list(frames)
