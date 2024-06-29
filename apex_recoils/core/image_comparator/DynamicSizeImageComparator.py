from apex_recoils.core.image_comparator.NetImageComparator import NetImageComparator
from apex_yolov5.log import LogFactory


class DynamicSizeImageComparator(NetImageComparator):
    """
        可动态模糊匹配的网络图片对比
    """

    def __init__(self, base_path, screen_taker):
        super().__init__(base_path)
        self.image_cache = {}
        self.logger = LogFactory.getLogger(self.__class__)
        self.base_path = base_path
        self.screen_taker = screen_taker

    def compare_with_path(self, path, images, lock_score, discard_score):
        path = self.base_path + path
        image_info_arr = [image_info.split() for image_info in
                          self.read_file_from_url_and_cache(path, "list.txt")]
        select_name, score_temp = self.match_template(path, image_info_arr, threshold=discard_score)
        return select_name, score_temp

    def match_template(self, path, image_info_arr, threshold=0.8):
        for image_info in image_info_arr:
            image_path, x, y, w, h = image_info
            image_path = path + image_path
            box = (int(x), int(y), int(w), int(h))
            img = self.screen_taker.get_images_from_bbox([box])[0]
            score = super().compare_image(img, image_path)
            if score > threshold:
                return image_info[0].split(".")[0], score
        return "", 0.0

    def cache_image(self, base_path, line_content):
        arr = line_content.split()
        if len(arr) == 5:
            image_path, x, y, w, h = arr[0], arr[1], arr[2], arr[3], arr[4]
            image_path = base_path + image_path
        else:
            image_path = line_content
        super().cache_image("", image_path)
