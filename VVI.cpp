#include <iostream> 
#include <chrono>
#define PACE 0
#define VB 1
#define VRP 2
#define LRLONLY 3

using namespace std;

// Function to get time in milliseconds
uint64_t millis(){
    using namespace chrono;
    return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}
// Function prototypes
class hardwareSys; 
void processPaceState(char &state);
void processVBState(char &state);
void processVRPState(char &state);
void processLRLOnlyState(char &state);

// Global class to simulate system io
static hardwareSys sys;

int main(){
    // Setup:
    char pState = LRLONLY;
    sys.setLRLTimer();

    // Loop
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
    if (!sys.VPaceTimerActive){
        sys.VPaceOn();
        sys.setVPaceTimer(); // also sets VPaceTimerActive to true
        return;   
    }
    // if pace timer expires, reset and change state
    if (sys.VPaceTimer_expired()){
        sys.VPaceOff();
        sys.clearVPaceTimer();
        state = VB;
        return;
    }
    return;
}
void processVBState(char &state){
    if (!sys.VBTimerActive){
        sys.setVBTimer();
        return;
    }
    if (sys.VBTimer_expired()){
        sys.clearVBTimer();
        state = VRP;
        return;
    }
    return;
}
void processVRPState(char &state){
    if (!sys.VRPTimerActive){
        sys.setVRPTimer();
        return;
    }
    if (sys.VRPTimer_expired()){
        sys.clearVRPTimer();
        state = LRLONLY;
        return;
    }
    return;

}
void processLRLOnlyState(char &state){
    if (sys.LRL_timer_expired()){
        sys.clearLRLTimer();
        sys.setLRLTimer();

        state = PACE;
        return;
    }
    if (sys.Ventricular_Sensed()){
        sys.clearLRLTimer();
        sys.setLRLTimer();
        state = VB;
        return;
    }
    return;
}

class hardwareSys{
    private:
        const long LRLInt = 1000;
        const long VPaceInt = 1000;
        const long VBInt = 1000;
        const long VRPInt = 1000;

        bool IO_VSensorActive = true;
        bool IO_PaceActive = false;

        bool LRLTimerActive = false;

        uint64_t LRLTimerEndValue;
        uint64_t VPaceTimerEndValue;
        uint64_t VBTimerEndValue;    
        uint64_t VRPTimerEndValue;

    public:
        hardwareSys(){}
        bool VPaceTimerActive = false;
        bool VBTimerActive = false;
        bool VRPTimerActive = false;

        // LRL Functions:
        bool LRL_timer_expired(){
            if(this->LRLTimerActive && millis() >= LRLTimerEndValue)
                return true;
            else
                return false;
        }
        void clearLRLTimer(){
            this->LRLTimerActive = false;
        }
        void setLRLTimer(){
            this->LRLTimerActive = true;
            this->LRLTimerEndValue = millis() + LRLInt;
        }

        // Sensing Functions:
        bool Ventricular_Sensed(){
            // Some IO event sensing
        }

        // VPace Functions: 
        void VPaceOn(){
            // FIRST disable sensor to protect it
            this->IO_VSensorActive = false;
            this->IO_PaceActive = true;
        }
        void VPaceOff(){
            this->IO_PaceActive = false;
        }
        void setVPaceTimer(){
            this->VPaceTimerActive = true;
            this->VPaceTimerEndValue = millis() + VPaceInt;
        }
        bool VPaceTimer_expired(){
            // V Pace timer has to be active and reach the end value to expire
            if(this->VPaceTimerActive = true && millis() >= VPaceTimerEndValue)
                return true;
            else
                return false;
        }
        void clearVPaceTimer(){
            this->VPaceTimerActive = false;
        }

        // VB Functions:
        void setVBTimer(){
            this->VBTimerActive = true;
            this->IO_VSensorActive = false;
            this->VBTimerEndValue = millis() + VBInt;
        }
        void clearVBTimer(){
            this->VBTimerActive = false;
            this->IO_VSensorActive = true;
        }
        bool VBTimer_expired(){
            if(this->VBTimerActive && millis() >= VBTimerEndValue)
                return true;
            else   
                return false;
        }

        // VRP Functions:
        void setVRPTimer(){
            this->VRPTimerActive = true;
            this->VRPTimerEndValue = millis() + VRPInt;
        }
        void clearVRPTimer(){
            this->VRPTimerActive = false;
        }
        bool VRPTimer_expired(){
            if (this->VRPTimerActive && millis() >= VRPTimerEndValue)
                return true;
            else
                return false;
        }

};