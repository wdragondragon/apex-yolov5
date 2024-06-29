import os

import cv2
import numpy as np
from skimage.metrics import structural_similarity

from apex_recoils.core.image_comparator.ImageComparator import ImageComparator
from apex_yolov5.log import LogFactory

net_file_cache = {}


class LocalImageComparator(ImageComparator):
    """
        本地图片对比
    """

    def __init__(self, base_path):
        super().__init__(base_path)
        self.image_cache = {}
        self.logger = LogFactory.getLogger(self.__class__)
        self.base_path = base_path

    def read_file_from_url(self, path):
        if path not in net_file_cache:
            net_file_cache[path] = [file for file in os.listdir(path) if file.endswith('.png') or file.endswith(".jpg")]
        return net_file_cache[path]

    def cache_image(self, base_path, url):
        # 如果图像已经在缓存中，直接返回缓存的图像
        url = base_path + url
        url = url.strip()
        if url in self.image_cache:
            return
        self.logger.print_log(f"正在加载图片：{url.replace(self.base_path, '')}")
        if os.path.exists(url) and os.path.isfile(url):
            self.image_cache[url] = np.fromfile(url, dtype=np.uint8)
        else:
            # 如果请求失败，打印错误信息
            self.logger.print_log(f"Failed to load image: {url}. check exists")

    def get_image_from_cache(self, url):
        """
            缓存获取图片
        """
        # 如果图像已经在缓存中，直接返回缓存的图像
        url = url.strip()
        if url not in self.image_cache:
            self.cache_image(url)
        return self.image_cache[url]

    def compare_image(self, img, path_image):
        """
            图片对比
        :param img:
        :param path_image:
        :return:
        """
        cache_image = self.image_cache.get(path_image)

        if cache_image:
            image_a = np.array(img)
            image_b = cv2.imdecode(cache_image, cv2.IMREAD_COLOR)
            gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
            gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
            (score, diff) = structural_similarity(gray_a, gray_b, full=True)
            return score
        else:
            return 0
