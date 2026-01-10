import concurrent.futures

from apex_yolov5.log import LogFactory
import concurrent.futures
import traceback
from io import BytesIO

import cv2
import numpy as np
from skimage.metrics import structural_similarity

class ImageComparator:
    """
        图片对比
    """

    def __init__(self, base_path):
        # 用于缓存图片
        self.image_cache = {}
        self.logger = LogFactory.getLogger(self.__class__)
        self.base_path = base_path

    def compare_image(self, img, path_image):
        """
            图片对比
        :param img:
        :param path_image:
        :return:
        """
        # 下载图片到内存
        try:
            downloaded_image = self.get_image_from_cache(path_image)

            if downloaded_image:
                downloaded_image.seek(0)
                image_a = cv2.imdecode(np.frombuffer(downloaded_image.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
                downloaded_image.close()
                image_b = np.array(img)
                gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
                gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
                (score, diff) = structural_similarity(gray_a, gray_b, full=True)
                return score
            else:
                # 图片下载失败时的处理
                return 0
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.logger.print_log(f"对比图片错误：{path_image}")
            return 0
    def get_image_from_cache(self, url):
        """
            缓存获取图片
        """
        # 如果图像已经在缓存中，直接返回缓存的图像
        url = url.strip()
        if url not in self.image_cache:
            self.cache_image("", url)
        return BytesIO(self.image_cache[url])


    def compare_with_path(self, path, images, lock_score, discard_score):
        """
            截图范围与文件路径内的所有图片对比
        :param path:
        :param images:
        :param lock_score:
        :param discard_score:
        :return:
        """
        path = self.base_path + path
        select_name = ''
        score_temp = 0.00000000000000000000
        for img in images:
            for fileName in self.read_file_from_url_and_cache(path, "list.txt"):
                score = self.compare_image(img, path + fileName)
                if score > score_temp:
                    score_temp = score
                    select_name = fileName.split('.')[0]
                if score_temp > lock_score:
                    break
        if score_temp < discard_score:
            select_name = None
        return select_name, score_temp

    def read_file_from_url_and_cache(self, base_path, file_name):
        """
            从文件中读取并下载图片
        """
        images_path = self.read_file_from_url(base_path + file_name)
        if images_path is None:
            return None

        # 使用线程池
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 提交每个下载任务给线程池
            futures = [executor.submit(self.cache_image, base_path, image_path) for image_path in images_path]

            # 等待所有任务完成
            concurrent.futures.wait(futures)

        return images_path

    def read_file_from_url(self, url):
        """
        :param url
        """
        return []

    def cache_image(self, base_path, url):
        """
        :param base_path:
        :param url:
        :return:
        """
        self.logger.print_log("Caching image is no working...")
        pass
