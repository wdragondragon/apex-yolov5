import mss

from apex_yolov5.log import LogFactory


class LocalMssScreenTaker:
    """
        本地截图
    """

    def __init__(self):
        self.logger = LogFactory.getLogger(self.__class__)

    def get_images_from_bbox(self, bbox_list):
        """
        Get images from specified bounding boxes.

        :param bbox_list: List of bounding boxes [(x1, y1, x2, y2), ...]
        :return: Generator yielding images
        """

        try:
            with mss.mss() as sct:
                return list(
                    sct.grab({'top': bbox[1], 'left': bbox[0], 'width': bbox[2] - bbox[0], 'height': bbox[3] - bbox[1]})
                    for bbox in bbox_list)
        except Exception as e:
            self.logger.print_log(f"Error in get_images_from_bbox: {e}")
