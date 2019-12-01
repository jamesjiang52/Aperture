"""
Utility module for sending Portal 2 input
"""


import time
import threading
import ctypes
import win32api
import win32con


# some constants
# TURN_INCREMENT = 100  # pixels
# MOVE_DURATION = 0.5  # seconds
MOVE_PAUSE = 0.05  # seconds

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
E = 0x12
SPACE = 0x39
MOUSE_LEFT = (0x0002, 0x0004)
MOUSE_RIGHT = (0x0008, 0x0010)


# ---------------------------- BEGIN CTYPES IMPLEMENTATION ----------------------------

def __pixels_to_windows_coordinates(_x, _y):
    return (
        (_x*65535)//win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN),
        (_y*65535)//win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    )


# ctypes struct definitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    # pylint: disable=missing-class-docstring,too-few-public-methods
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class HardwareInput(ctypes.Structure):
    # pylint: disable=missing-class-docstring,too-few-public-methods
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]


class MouseInput(ctypes.Structure):
    # pylint: disable=missing-class-docstring,too-few-public-methods
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class InputI(ctypes.Union):
    # pylint: disable=missing-class-docstring,too-few-public-methods
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]


class Input(ctypes.Structure):
    # pylint: disable=missing-class-docstring,too-few-public-methods
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", InputI)
    ]


def __press_key(key_hex_code):
    # pylint: disable=invalid-name,attribute-defined-outside-init
    extra = ctypes.c_ulong(0)
    ii = InputI()
    ii.ki = KeyBdInput(0, key_hex_code, 0x0008, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(1), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))


def __release_key(key_hex_code):
    # pylint: disable=invalid-name,attribute-defined-outside-init
    extra = ctypes.c_ulong(0)
    ii = InputI()
    ii.ki = KeyBdInput(0, key_hex_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(1), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))


def __click(button_hex_code):
    # pylint: disable=invalid-name,attribute-defined-outside-init
    extra = ctypes.c_ulong(0)
    ii = InputI()
    ii.mi = MouseInput(0, 0, 0, button_hex_code, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(0), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))


def __move_cursor(x, y):
    # pylint: disable=invalid-name,attribute-defined-outside-init
    extra = ctypes.c_ulong(0)
    ii = InputI()
    ii.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(0), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))

# ---------------------------- END CTYPES IMPLEMENTATION ----------------------------


def __tap_key(hex_code):
    """
    Tap the key with the given hex code
    :param hex_code: int
    :return: None
    """
    __press_key(hex_code)
    time.sleep(MOVE_PAUSE)
    __release_key(hex_code)


def __do_look_operation(delta):
    """
    Move the cursor x pixels to the right and y pixels down,
        where (x, y) = delta
    :param delta: (int, int) tuple
    :return: None
    """
    __move_cursor(*delta)


def __do_move_operation(hex_code, duration):
    """
    Repeatedly tap the key with the given hex code for the
        given duration
    :param hex_code: int
    :param duration: float
    :return: None
    """
    start = time.time()
    while time.time() - start < duration:
        __tap_key(hex_code)


def __do_shoot_portal_operation(event_codes):
    """
    Tap the mouse button corresponding to event_codes[0] for the
        mouse down event and event_codes[1] for the mouse up event
    :param event_codes: (int, int) tuple
    :return: None
    """
    __click(event_codes[0])
    __click(event_codes[1])


def look_up(increment):
    """
    Move the cursor up by the given number of pixels
    :param increment: int
    :return: None
    """
    threading.Thread(target=__do_look_operation, args=((0, -increment),)).start()


def look_down(increment):
    """
    Move the cursor down by the given number of pixels
    :param increment: int
    :return: None
    """
    threading.Thread(target=__do_look_operation, args=((0, increment),)).start()


def look_left(increment):
    """
    Move the cursor left by the given number of pixels
    :param increment: int
    :return: None
    """
    threading.Thread(target=__do_look_operation, args=((-increment, 0),)).start()


def look_right(increment):
    """
    Move the cursor right by the given number of pixels
    :param increment: int
    :return: None
    """
    threading.Thread(target=__do_look_operation, args=((increment, 0),)).start()


def move_forwards(duration):
    """
    Repeatedly press the W key for the given duration
    :param duration: float (in seconds)
    :return: None
    """
    threading.Thread(target=__do_move_operation, args=(W, duration)).start()


def move_backwards(duration):
    """
    Repeatedly press the S key for the given duration
    :param duration: float (in seconds)
    :return: None
    """
    threading.Thread(target=__do_move_operation, args=(S, duration)).start()


def move_left(duration):
    """
    Repeatedly press the A key for the given duration
    :param duration: float (in seconds)
    :return: None
    """
    threading.Thread(target=__do_move_operation, args=(A, duration)).start()


def move_right(duration):
    """
    Repeatedly press the D key for the given duration
    :param duration: float (in seconds)
    :return: None
    """
    threading.Thread(target=__do_move_operation, args=(D, duration)).start()


def jump():
    """
    Tap the spacebar
    :return: None
    """
    threading.Thread(target=__tap_key, args=(SPACE,)).start()


def interact():
    """
    Tap the E key
    :return: None
    """
    threading.Thread(target=__tap_key, args=(E,)).start()


def shoot_blue_portal():
    """
    Click the left mouse button
    :return: None
    """
    threading.Thread(target=__do_shoot_portal_operation, args=(MOUSE_LEFT,)).start()


def shoot_orange_portal():
    """
    Click the right mouse button
    :return: None
    """
    threading.Thread(target=__do_shoot_portal_operation, args=(MOUSE_RIGHT,)).start()


def run_and_sleep(func, *args, **kwargs):
    """
    Run the function with the given arguments, then sleep for 1 sec
    """
    func(*args, **kwargs)
    time.sleep(1)


def __test_all_operations():
    time.sleep(5)

    run_and_sleep(look_up, 100)
    run_and_sleep(look_down, 50)
    run_and_sleep(look_left, 100)
    run_and_sleep(look_right, 50)

    run_and_sleep(move_forwards, 1)
    run_and_sleep(move_backwards, 0.5)
    run_and_sleep(move_left, 1)
    run_and_sleep(move_right, 0.5)
    run_and_sleep(jump)

    run_and_sleep(interact)
    run_and_sleep(shoot_blue_portal)
    run_and_sleep(shoot_orange_portal)


if __name__ == "__main__":
    __test_all_operations()


# ----------------- BEGIN REVAMP -----------------

CAMERA_INSTANT = 11111
CAMERA_FAST = 22222
CAMERA_SLOW = 33333
CAMERA_NUDGE = 44444

def move_camera(delta, speed=CAMERA_FAST):
    # does some stuff asynchronously
    pass


def stop_camera():
    pass


def move_forward(tap=False):
    pass


def stop_move_forward():
    pass


def move_backward(tap=False):
    pass


def stop_move_backward():
    pass


def move_left(tap=False):
    pass


def stop_move_left():
    pass


def move_right(tap=False):
    pass


def stop_move_right():
    pass
