#ifndef _INPUT_CONTROLLER_H_
#define _INPUT_CONTROLLER_H_

struct ControllerImpl;

enum class MovementOption {
    Hold = 1, Tap = 2
};

enum class CameraOption {
    Instant = 11, Fast = 12, Slow = 13, Nudge = 14
};

class Controller {

    private:
        ControllerImpl* impl;
        
    public:
        Controller();
        ~Controller();

        void forward(MovementOption option);
        void backward(MovementOption option);
        void left(MovementOption option);
        void right(MovementOption option);
        void stop();

        void jump();
        void interact();
        void bluePortal();
        void orangePortal();

        void camera(long dx, long dy, CameraOption option);
        void stopCamera();
};

#endif
