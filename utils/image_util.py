import cv2
import numpy as np


def crop_and_restore_image(image, x, y, w, h):
    """
        切图
    """
    # 获取图片的高度和宽度
    height, width = image.shape[:2]

    # 检查裁剪区域是否在图片范围内
    if x + w > width or y + h > height:
        raise ValueError("裁剪区域超出图片范围")

    # 裁剪图片
    cropped_image = image[y:y + h, x:x + w]

    # 创建一个与原图大小相同的空白图片
    result_image = np.zeros_like(image)

    # 将裁剪后的图片放置到原图相同位置
    result_image[y:y + h, x:x + w] = cropped_image

    return result_image


def crop_center(image, target_width, target_height):
    """
        以图片中心开始切分
    """
    # 获取图片的高度和宽度
    height, width = image.shape[:2]

    # 计算中心点
    center_x, center_y = width // 2, height // 2

    # 计算裁剪区域的左上角坐标
    x = max(0, center_x - target_width // 2)
    y = max(0, center_y - target_height // 2)

    # 确保裁剪区域不超出图片边界
    x_end = min(width, x + target_width)
    y_end = min(height, y + target_height)

    # 计算实际的裁剪宽度和高度
    actual_width = x_end - x
    actual_height = y_end - y

    # 裁剪图片
    cropped_image = image[y:y + actual_height, x:x + actual_width]

    return cropped_image


def crop_center_xy(image, target_width, target_height, xyxy):
    # 获取图片的高度和宽度
    height, width = image.shape[:2]

    # 计算中心点
    center_x, center_y = width // 2, height // 2

    # 计算裁剪区域的左上角坐标
    x = max(0, center_x - target_width // 2)
    y = max(0, center_y - target_height // 2)

    return xyxy[0] + x, xyxy[1] + y, xyxy[2] + x, xyxy[3] + y
