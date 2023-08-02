import mss

import time

from PIL import ImageGrab

with mss.mss() as sct:
    monitor = {'top': 0, 'left': 0, 'width': 600, 'height': 600}
    # bbox = (0, 0, 600, 600)
    last_time = time.time()
    n = 400
    for i in range(n):
        # ImageGrab.grab(bbox=bbox)
        img = sct.grab(monitor)
    print("fps: {}".format(400 / (time.time() - last_time)))
