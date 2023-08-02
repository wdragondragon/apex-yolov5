import cv2
from mss import mss
from io import BytesIO
import numpy as np

sct = mss()


def grab_screen(monitor=None):
    img = sct.grab(monitor)
    screenshot = np.array(img)
    return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
