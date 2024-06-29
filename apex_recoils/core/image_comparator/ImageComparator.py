import concurrent.futures

from apex_yolov5.log import LogFactory


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
        return 0

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
