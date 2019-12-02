#define WINVER 0x0A00
#define _WIN32_WINNT 0x0A00

#include <windows.h>

#include <new>
#include <thread>
#include <atomic>

#include "input_controller.h"

#define MOVE_PAUSE 40

#define KEY_W 0x11
#define KEY_A 0x1E
#define KEY_S 0x1F
#define KEY_D 0x20
#define KEY_E 0x12
#define KEY_SPACE 0x39

#define MOUSE_LEFT_DOWN 0x0002
#define MOUSE_LEFT_UP 0x0004
#define MOUSE_RIGHT_DOWN 0x0008
#define MOUSE_RIGHT_UP 0x0010

#define NUDGE_PIXELS 6
#define CAMERA_FAST_PIXELS 5
#define CAMERA_SLOW_PIXELS 2

struct ControllerImpl {
    std::atomic_bool movementStopRequested{false};
    std::atomic_bool cameraStopRequested{false};

    void pressKey(WORD keyCode) {
        INPUT i;
        i.type = INPUT_KEYBOARD;
        i.ki = KEYBDINPUT{0, keyCode, KEYEVENTF_SCANCODE, 0, 0};
        SendInput(1, &i, sizeof(INPUT));
    }

    void releaseKey(WORD keyCode) {
        INPUT i;
        i.type = INPUT_KEYBOARD;
        i.ki = KEYBDINPUT{0, keyCode, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, 0};
        SendInput(1, &i, sizeof(INPUT));
    }
        
    void click(DWORD keyCode) {
        INPUT i;
        i.type = INPUT_MOUSE;
        i.mi = MOUSEINPUT{0, 0, 0, keyCode, 0, 0};
        SendInput(1, &i, sizeof(INPUT));
    }
        
    void moveCursor(LONG x, LONG y) {
        INPUT i;
        i.type = INPUT_MOUSE;
        i.mi = MOUSEINPUT{x, y, 0, MOUSEEVENTF_MOVE, 0, 0};
        SendInput(1, &i, sizeof(INPUT));
    }
        
    void tapKey(WORD keyCode) {
        pressKey(keyCode);
        Sleep(MOVE_PAUSE);
        releaseKey(keyCode);
    }
        
    void holdForward() {
        while (!movementStopRequested) {
            tapKey(KEY_W);
        }
        movementStopRequested = false;
    }

    void holdBackward() {
        while (!movementStopRequested) {
            tapKey(KEY_S);
        }
        movementStopRequested = false;
    }

    void holdLeft() {
        while (!movementStopRequested) {
            tapKey(KEY_A);
        }
        movementStopRequested = false;
    }

    void holdRight() {
        while (!movementStopRequested) {
            tapKey(KEY_D);
        }
        movementStopRequested = false;
    }

    void cameraFast(LONG dx, LONG dy) {
        long x = 0, y = 0, ndx = 0, ndy = 0;
        long inc = CAMERA_FAST_PIXELS;
        while (!cameraStopRequested) {
            ndx = dx * inc / (dx + dy) - x;
            ndy = dx * inc / (dx + dy) - y;
            moveCursor(ndx, ndy);
            x += ndx;
            y += ndy;
            inc += CAMERA_FAST_PIXELS;
            Sleep(1);
        }
        cameraStopRequested = false;
    }

    void cameraSlow(LONG dx, LONG dy) {
        long x = 0, y = 0, ndx = 0, ndy = 0;
        long inc = CAMERA_SLOW_PIXELS;
        while (!cameraStopRequested) {
            ndx = dx * inc / (dx + dy) - x;
            ndy = dx * inc / (dx + dy) - y;
            moveCursor(ndx, ndy);
            x += ndx;
            y += ndy;
            inc += CAMERA_SLOW_PIXELS;
            Sleep(1);
        }
        cameraStopRequested = false;
    }
};

Controller::Controller() {
    impl = new ControllerImpl;
}

Controller::~Controller() {
    delete impl;
}
    
void Controller::forward(MovementOption option) {
    switch (option) {
        case MovementOption::Hold:
            std::thread(impl->holdForward).detach();
            break;
        case MovementOption::Tap:
            std::thread(impl->tapKey, KEY_W).detach();
            break;
    }
}
        
void Controller::backward(MovementOption option) {
    switch (option) {
        case MovementOption::Hold:
            std::thread(impl->holdBackward).detach();
            break;
        case MovementOption::Tap:
            std::thread(impl->tapKey, KEY_S).detach();
            break;
    }
}

void Controller::left(MovementOption option) {
    switch (option) {
        case MovementOption::Hold:
            std::thread(impl->holdLeft).detach();
            break;
        case MovementOption::Tap:
            std::thread(impl->tapKey, KEY_A).detach();
            break;
    }
}

void Controller::right(MovementOption option) {
    switch (option) {
        case MovementOption::Hold:
            std::thread(impl->holdRight).detach();
            break;
        case MovementOption::Tap:
            std::thread(impl->tapKey, KEY_D).detach();
            break;
    }
}

void Controller::stop() {
    impl->movementStopRequested = true;
}
        
void Controller::jump() {
    std::thread(impl->tapKey, KEY_SPACE).detach();
}
        
void Controller::interact() {
    std::thread(impl->tapKey, KEY_E).detach();
}

void Controller::bluePortal() {
    impl->click(MOUSE_LEFT_DOWN);
    impl->click(MOUSE_LEFT_UP);
}

void Controller::orangePortal() {
    impl->click(MOUSE_RIGHT_DOWN);
    impl->click(MOUSE_RIGHT_UP);
}

void Controller::camera(long dx, long dy, CameraOption option) {
    switch (option) {
        case CameraOption::Instant:
            impl->moveCursor(dx, dy);
            break;
        case CameraOption::Fast:
            std::thread(impl->cameraFast, dx, dy).detach();
            break;
        case CameraOption::Slow:
            std::thread(impl->cameraSlow, dx, dy).detach();
            break;
        case CameraOption::Nudge:
            impl->moveCursor(dx * NUDGE_PIXELS / (dx + dy), dy * NUDGE_PIXELS / (dx + dy));
            break;
    }
}

void Controller::stopCamera() {
    impl->cameraStopRequested = true;
}

extern "C" {

    int MOVE_HOLD = 1;
    int MOVE_TAP = 2;
    int CAMERA_INSTANT = 11;
    int CAMERA_FAST = 12;
    int CAMERA_SLOW = 13;
    int CAMERA_NUDGE = 14;

    void* CreateController() {
        return new(std::nothrow) Controller;
    }

    void DeleteController(void* controller) {
        delete reinterpret_cast<Controller*>(controller);
    }

    void forward(void* controller, int option) {
        reinterpret_cast<Controller*>(controller)->forward(static_cast<MovementOption>(option));
    }

    void backward(void* controller, int option) {
        reinterpret_cast<Controller*>(controller)->backward(static_cast<MovementOption>(option));
    }

    void left(void* controller, int option) {
        reinterpret_cast<Controller*>(controller)->left(static_cast<MovementOption>(option));
    }

    void right(void* controller, int option) {
        reinterpret_cast<Controller*>(controller)->right(static_cast<MovementOption>(option));
    }

    void freeze(void* controller) {
        reinterpret_cast<Controller*>(controller)->stop();
    }

    void jump(void* controller) {
        reinterpret_cast<Controller*>(controller)->jump();
    }

    void interact(void* controller) {
        reinterpret_cast<Controller*>(controller)->interact();
    }

    void blue(void* controller) {
        reinterpret_cast<Controller*>(controller)->bluePortal();
    }

    void orange(void* controller) {
        reinterpret_cast<Controller*>(controller)->orangePortal();
    }

    void camera(void* controller, long dx, long dy, int option) {
        reinterpret_cast<Controller*>(controller)->camera(dx, dy, static_cast<CameraOption>(option));
    }

    void stop(void* controller) {
        reinterpret_cast<Controller*>(controller)->stopCamera();
    }
}




