import os
import re

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


    def read_file_from_url(self, filepath):
        """
        从本地文件读取内容并按行返回
        :param filepath: 本地文件路径
        :return: 按行分割后的字符串列表，或 None（失败时）
        """
        try:
            if filepath in net_file_cache:
                return net_file_cache[filepath]

            if not os.path.isfile(filepath):
                print(f"File not found: {filepath}")
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

                lines = re.split(r'\r\n|\r|\n', text)
                net_file_cache[filepath] = lines
                return lines
        except Exception as e:
            print(f"An error occurred while reading local file: {e}")
            return None

    def cache_image(self, base_path, url):
        # 如果图像已经在缓存中，直接返回缓存的图像
        url = base_path + url
        url = url.strip()
        if url in self.image_cache:
            return
        self.logger.print_log(f"正在加载图片：{url.replace(self.base_path, '')}")
        if os.path.exists(url) and os.path.isfile(url):
            with open(url, 'rb') as f:
                self.image_cache[url] = f.read()
        else:
            # 如果请求失败，打印错误信息
            self.logger.print_log(f"Failed to load image: {url}. check exists")