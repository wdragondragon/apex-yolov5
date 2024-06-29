import threading
import time
import traceback

from apex_recoils.core.screentaker.LocalScreenTaker import LocalScreenTaker
from apex_yolov5.KeyAndMouseListener import KMCallBack
from apex_yolov5.log import LogFactory


class SelectGun:
    """
        枪械识别
    """

    def __init__(self, bbox, image_path, scope_bbox, scope_path, hop_up_bbox, hop_up_path,
                 refresh_buttons, has_turbocharger, image_comparator, screen_taker: LocalScreenTaker,
                 game_windows_status):
        super().__init__()
        self.logger = LogFactory.getLogger(self.__class__)
        self.on_key_map = dict()
        self.bbox = bbox
        self.image_path = image_path
        self.scope_bbox = scope_bbox
        self.scope_path = scope_path
        self.select_gun_sign = True
        self.current_gun = None
        self.current_scope = None
        self.current_hot_pop = None
        self.real_current_scope = None
        self.refresh_buttons = refresh_buttons
        self.has_turbocharger = has_turbocharger
        self.hop_up_bbox = hop_up_bbox
        self.hop_up_path = hop_up_path
        self.game_windows_status = game_windows_status
        self.call_back = []
        self.fail_time = 0
        self.image_comparator = image_comparator
        self.screen_taker = screen_taker
        for refresh_button in self.refresh_buttons:
            KMCallBack.connect(KMCallBack("k", refresh_button, self.select_gun_threading, False))

        threading.Thread(target=self.timing_execution).start()

    def timing_execution(self):
        """
            定时识别
        """
        while True:
            try:
                if self.game_windows_status.get_game_windows_status():
                    if self.select_gun_with_sign(auto=True):
                        self.fail_time = 0
                    else:
                        self.fail_time += 1
                else:
                    self.fail_time = 0
            except Exception as e:
                traceback.print_exc()
                pass
            time.sleep(1 + self.fail_time / 5)

    def select_gun_threading(self, pressed=False, toggle=False):
        """

        :param pressed:
        :param toggle:
        :return:
        """
        if self.select_gun_sign:
            return
        threading.Thread(target=self.select_gun_with_sign, args=(pressed, toggle, False)).start()

    def select_gun_with_sign(self, pressed=False, toggle=False, auto=False):
        """

        :param pressed:
        :param toggle:
        :param auto:
        :return:
        """
        if self.select_gun_sign:
            return
        self.select_gun_sign = True
        start = time.time()
        result = self.select_gun(pressed, toggle, auto)
        self.logger.print_log(f"该次识别耗时：{int((time.time() - start) * 1000)}ms")
        self.select_gun_sign = False
        return result

    def get_images_from_bbox(self, bbox_list):
        """
        Get images from specified bounding boxes.

        :param bbox_list: List of bounding boxes [(x1, y1, x2, y2), ...]
        :return: Generator yielding images
        """
        # try:
        #     return list(ImageGrab.grab(bbox=bbox) for bbox in bbox_list)
        # except Exception as e:
        #     self.logger.print_log(f"Error in get_images_from_bbox: {e}")
        return self.screen_taker.get_images_from_bbox(bbox_list)

    def select_gun(self, pressed=False, toggle=False, auto=False):
        """
            使用图片对比，逐一识别枪械，相似度最高设置为current_gun
        :return:
        """
        if not self.game_windows_status.get_game_windows_status():
            return False
        gun_temp, score_temp = self.image_comparator.compare_with_path(self.image_path,
                                                                       self.get_images_from_bbox([self.bbox]), 0.9, 0.7)
        if gun_temp is None:
            self.logger.print_log("未找到枪械")
            self.current_gun = None
            self.current_scope = None
            self.current_hot_pop = None
            return False

        scope_temp, score_scope_temp = self.image_comparator.compare_with_path(self.scope_path,
                                                                               self.get_images_from_bbox(
                                                                                   self.scope_bbox), 0.9,
                                                                               0.4)
        self.real_current_scope = scope_temp
        if scope_temp is None:
            self.logger.print_log("未找到配件，默认为1倍")
            scope_temp = '1x'

        if gun_temp in self.has_turbocharger:
            hop_up_temp, score_hop_up_temp = self.image_comparator.compare_with_path(self.hop_up_path,
                                                                                     self.get_images_from_bbox(
                                                                                         self.hop_up_bbox),
                                                                                     0.9, 0.6)
        else:
            hop_up_temp = None
            score_hop_up_temp = 0

        if gun_temp == self.current_gun and scope_temp == self.current_scope and hop_up_temp == self.current_hot_pop:
            self.logger.print_log(
                "当前枪械搭配已经是: {}-{}-{}".format(self.current_gun, self.current_scope, self.current_hot_pop))
            if auto:
                return False
        else:
            self.current_scope = scope_temp
            self.current_gun = gun_temp
            self.current_hot_pop = hop_up_temp
            self.logger.print_log(
                "枪械: {},相似: {}-配件: {},相似: {}-hop_up: {},相似: {}".format(self.current_gun, score_temp,
                                                                                 self.current_scope, score_scope_temp,
                                                                                 self.current_hot_pop,
                                                                                 score_hop_up_temp))

        for func in self.call_back:
            func(self.current_gun, self.current_scope, self.current_hot_pop)
        return True

    def connect(self, func):
        self.call_back.append(func)

    def test(self):
        self.logger.print_log("自动识别初始化中，请稍后……")
        start = time.time()
        self.image_comparator.compare_with_path(self.image_path,
                                                self.get_images_from_bbox([self.bbox]), 0.9, 0.7)
        self.image_comparator.compare_with_path(self.scope_path,
                                                self.get_images_from_bbox(
                                                    self.scope_bbox), 0.9,
                                                0.4)
        self.image_comparator.compare_with_path(self.hop_up_path,
                                                self.get_images_from_bbox(
                                                    self.hop_up_bbox),
                                                0.9, 0.6)
        self.logger.print_log(f"自动识别初始化完毕，耗时[{int((time.time() - start) * 1000)}]")
        self.select_gun_sign = False


select_gun = None


def get_select_gun():
    return select_gun
