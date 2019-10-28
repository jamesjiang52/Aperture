import threading
import ctypes
import win32api
import win32con
import time

# some constants
TURN_INCREMENT = 100  # pixels
MOVE_DURATION = 0.5  # seconds
MOVE_PAUSE = 0.1  # seconds

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
MOUSE_LEFT = (0x0002, 0x0004)
MOUSE_RIGHT = (0x0008, 0x0010)


def __pixels_to_windows_coordinates(x, y):
    return (
        (x*65535)//win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN),
        (y*65535)//win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    )

# ctypes struct definitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time",ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]


def __press_key(key_hex_code):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.ki = KeyBdInput(0, key_hex_code, 0x0008, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(1), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))

def __release_key(key_hex_code):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.ki = KeyBdInput(0, key_hex_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(1), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))

def __click_down(button_hex_code):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.mi = MouseInput(0, 0, 0, button_hex_code, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(0), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))

def __click_up(button_hex_code):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.mi = MouseInput(0, 0, 0, button_hex_code, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(0), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))
    
def __move_cursor(x, y):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))
    i = Input(ctypes.c_ulong(0), ii)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(i), ctypes.sizeof(i))


def __do_look_operation(arg):
    __move_cursor(*arg)

def look_up():
    """Move cursor up a distance of TURN_INCREMENT pixels.
    """
    threading.Thread(target=__do_look_operation, args=((0, -TURN_INCREMENT),)).start()

def look_down():
    """Move cursor down a distance of TURN_INCREMENT pixels.
    """
    threading.Thread(target=__do_look_operation, args=((0, TURN_INCREMENT),)).start()

def look_left():
    """Move cursor left a distance of TURN_INCREMENT pixels.
    """
    threading.Thread(target=__do_look_operation, args=((-TURN_INCREMENT, 0),)).start()

def look_right():
    """Move cursor right a distance of TURN_INCREMENT pixels.
    """
    threading.Thread(target=__do_look_operation, args=((TURN_INCREMENT, 0),)).start()


def __do_move_operation(arg):
    start = time.time()
    while time.time() - start < MOVE_DURATION:
        __press_key(arg)
        time.sleep(MOVE_PAUSE)
        __release_key(arg)

def move_forwards():
    """Repeatedly press the W key for MOVE_DURATION seconds, with an interval
    of MOVE_PAUSE seconds between each press.
    """
    threading.Thread(target=__do_move_operation, args=(W,)).start()

def move_backwards():
    """Repeatedly press the S key for MOVE_DURATION seconds, with an interval
    of MOVE_PAUSE seconds between each press.
    """
    threading.Thread(target=__do_move_operation, args=(S,)).start()

def move_left():
    """Repeatedly press the A key for MOVE_DURATION seconds, with an interval
    of MOVE_PAUSE seconds between each press.
    """
    threading.Thread(target=__do_move_operation, args=(A,)).start()

def move_right():
    """Repeatedly press the D key for MOVE_DURATION seconds, with an interval
    of MOVE_PAUSE seconds between each press.
    """
    threading.Thread(target=__do_move_operation, args=(D,)).start()


def __do_shoot_portal_operation(arg):
    __click_down(arg[0])
    __click_up(arg[1])

def shoot_blue_portal():
    """Click the left mouse button.
    """
    threading.Thread(target=__do_shoot_portal_operation, args=(MOUSE_LEFT,)).start()

def shoot_orange_portal():
    """Click the right mouse button.
    """
    threading.Thread(target=__do_shoot_portal_operation, args=(MOUSE_RIGHT,)).start()


def __test_all_operations():
    time.sleep(5)

    operations = [
        look_up, look_down, look_left, look_right,
        move_forwards, move_backwards, move_left, move_right,
        shoot_blue_portal, shoot_orange_portal
    ]

    for operation in operations:
        operation()
        time.sleep(1)


if __name__ == "__main__":
    __test_all_operations()
