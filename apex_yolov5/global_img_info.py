class ImgInfo:
    def __init__(self, img_origin, img_data):
        self.img_origin = img_origin
        self.shot_width = img_origin.width
        self.shot_height = img_origin.height
        self.img_data = img_data


current_img = None


def set_current_img(img_origin, img_data):
    global current_img
    current_img = ImgInfo(img_origin, img_data)


def get_current_img():
    global current_img
    return current_img
