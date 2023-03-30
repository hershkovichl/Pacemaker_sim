#include <iostream> 
#define PACE 0
#define VB 1
#define VRP 2
#define LRLONLY 3

using namespace std;

// Function prototypes
class hardwareIO; 
void processPaceState(char &state);
void processVBState(char &state);
void processVRPState(char &state);
void processLRLOnlyState(char &state);

// Global class to simulate system io
hardwareIO io;

int main(){
    char pState;
    while(true){
        switch (pState){
            case PACE:
                processPaceState(pState);
                break;
            case VB:
                processVBState(pState);
                break;
            case VRP:
                processVRPState(pState);
                break;
            case LRLONLY:
                processLRLOnlyState(pState);
                break;
            default:
                throw std::invalid_argument("Invalid State");
                break;
        }
    }
}

void processPaceState(char &state){
    // if pace timer is off, start it
    if (!io.VPaceTimer_ison){
        io.VPaceOn();
        io.setVPaceTimer(); // also sets VPaceTimer_ison to true
        return;   
    }
    // if pace timer expires, reset and change state
    if (io.VPaceTimer_expired()){
        io.VPaceOff();
        io.clearVPaceTimer();
        state = VB;
        return;
    }
    return;
}
void processVBState(char &state){
    if (!io.VBTimer_ison){
        io.setVBTimer();
        return;
    }
    if (io.VBTimer_expired()){
        io.clearVBTimer();
        state = VRP;
        return;
    }
    return;
}
void processVRPState(char &state){
    if (!io.VRPTimer_ison){
        io.setVRPTimer();
        return;
    }
    if (io.VRPTimer_expired()){
        io.clearVRPTimer();
        state = LRLONLY;
        return;
    }
    return;

}
void processLRLOnlyState(char &state){
    if (io.LRL_timer_expired()){
        io.clearLRLTimer();
        io.setLRLTimer();

        state = PACE;
        return;
    }
    if (io.Ventricular_Sensed()){
        io.clearLRLTimer();
        io.setLRLTimer();
        state = VB;
        return;
    }
    return;
}


class hardwareIO{
    private:
        bool VSensorActive = true;
    public:
        hardwareIO(){
        }
        bool VPaceTimer_ison = false;
        bool VBTimer_ison = false;
        bool VRPTimer_ison = false;

        // LRL Functions:
        bool LRL_timer_expired(){}
        void clearLRLTimer(){}
        void setLRLTimer(){}

        // Sensing Functions:
        bool Ventricular_Sensed(){}

        // VPace Functions: 
        void VPaceOn(){}
        void VPaceOff(){}
        void setVPaceTimer(){
            this->VPaceTimer_ison = true;
        }
        bool VPaceTimer_expired(){}
        void clearVPaceTimer(){
            this->VPaceTimer_ison = false;
        }

        // VB Functions:
        void setVBTimer(){
            this->VSensorActive = false;
        }
        void clearVBTimer(){
            this->VSensorActive = true;
        }
        bool VBTimer_expired(){}

        // VRP Functions:
        void setVRPTimer(){}
        void clearVRPTimer(){}
        bool VRPTimer_expired(){}

};