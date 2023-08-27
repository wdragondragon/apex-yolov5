import os

from PIL import ImageGrab

from apex_yolov5.Tools import Tools
from apex_yolov5.socket.config import global_config


class SelectGun:
    def __init__(self, bbox, image_path):
        super().__init__()
        self.on_key_map = dict()
        self.bbox = bbox
        self.image_path = image_path
        self.select_gun_sign = False
        self.current_gun = ''

    def select_gun(self):
        if self.select_gun_sign:
            return
        self.select_gun_sign = True
        score_temp = 0.00000000000000000000
        img = ImageGrab.grab(bbox=self.bbox)
        gun_temp = ''
        for fileName in os.listdir(self.image_path):
            score = Tools.compare_image(img, self.image_path + fileName)
            if score > score_temp:
                score_temp = score
                gun_temp = fileName.split('.')[0]
            if score_temp > 0.9:
                break
        if gun_temp == self.current_gun:
            print("当前枪械已经是: {}".format(self.current_gun))
            self.select_gun_sign = False
            return
        self.current_gun = gun_temp
        print("枪械: {}, 最大相似度: {}".format(self.current_gun, score_temp))
        self.select_gun_sign = False


select_gun = SelectGun(global_config.select_gun_bbox, global_config.image_path)
