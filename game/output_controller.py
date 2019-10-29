import numpy as np
import mss
import time

sct = mss.mss()


def get_screenshot():
    # img has height equal to screen height and width equal to screen width
    # (currently 640x480)
    # each element of img is an array of BGRA values, which we convert to RGB
    img = np.array(sct.grab(sct.monitors[0]), dtype=np.uint8)
    return np.flip(img[:, :, :3], 2)


if __name__ == "__main__":
    time.sleep(5)
    img = get_screenshot()
    print("Game resolution is {}x{}".format(len(img[0]), len(img)))
