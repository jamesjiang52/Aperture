"""
Utility module for getting Portal 2 output
"""

import time
import numpy as np
import mss


SCT = mss.mss()


def get_screenshot():
    """
    Get a numpy array representing the RGB values of every pixel
        currently displaying in the window
    :return: m x n x 3 numpy array, where m is the screen height and
        n is the screen width
    """
    img = np.array(SCT.grab(SCT.monitors[0]), dtype=np.uint8)
    return np.flip(img[:, :, :3], axis=2)


def main():
    """
    Entry point if run as a script
    :return: None
    """
    time.sleep(5)
    img = get_screenshot()
    print("Game resolution is {}x{}".format(len(img[0]), len(img)))


if __name__ == "__main__":
    main()
