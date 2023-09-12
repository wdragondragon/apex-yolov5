import mss
import time
from apex_yolov5.grabscreen import grab_screen_int_array2
from apex_yolov5.socket.config import global_config

# 初始化计数器和时间戳
screenshot_count = 0
start_time = time.time()

with mss.mss() as sct:
    while True:
        img_origin = grab_screen_int_array2(sct, monitor=global_config.monitor)
        screenshot_count += 1

        # 计算经过的时间
        current_time = time.time()
        elapsed_time = current_time - start_time

        # 如果经过了一秒，则输出截图次数并重新计数
        if elapsed_time >= 1.0:
            print(f"Screenshots per second: {screenshot_count}")
            screenshot_count = 0
            start_time = current_time
