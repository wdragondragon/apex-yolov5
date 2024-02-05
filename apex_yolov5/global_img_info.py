class ImgInfo:
    def __init__(self):
        self.img_origin = None
        self.shot_width = None
        self.shot_height = None
        self.img_data = None

    def set_img_origin(self, img_origin, img_data):
        self.img_origin = img_origin
        self.shot_width = img_origin.width
        self.shot_height = img_origin.height
        self.img_data = img_data

    def set_img_origin_2(self, img_origin, img_data, shot_width, shot_height):
        self.img_origin = img_origin
        self.shot_width = shot_width
        self.shot_height = shot_height
        self.img_data = img_data


current_img = None


def set_current_img(img_origin, img_data):
    global current_img
    current_img = ImgInfo()
    current_img.set_img_origin(img_origin, img_data)


def set_current_img_2(img_origin, img_data, shot_width, shot_height):
    global current_img
    current_img = ImgInfo()
    current_img.set_img_origin_2(img_origin, img_data, shot_width, shot_height)


def get_current_img():
    global current_img
    return current_img
