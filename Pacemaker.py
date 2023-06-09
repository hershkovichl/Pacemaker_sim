from time import time
from heart_activity import POLARIZED, DEPOLARIZING, REFRACTORY, REPOLARIZING, FIBRILLATION, AFIB

class ModeSwitching:
    def __init__(self, heart):
        self.heart = heart
        self.sys = HardwareSystem(heart)
        self.VVI = VVI(self.sys)
        self.VDD = VDD(self.sys)
        self.time_of_last_AFib = 0
        self.AFib_Check_Period = 2000
        self.Mode = ''

    def check_for_AFib(self):
        if self.heart.rhythm.A_state == AFIB:
            self.time_of_last_AFib = time()

    def recent_AFib(self):
        if (time() - self.time_of_last_AFib) * 1000 <= self.AFib_Check_Period:
            return True
        else:
            return False

    def run(self):
        # Determine which state it's in
        self.check_for_AFib()
        if self.recent_AFib():
            self.Mode = 'VVI'
            self.VVI.run()
        else:
            self.VDD.run()
            self.Mode = 'VDD'
        return self.sys.IO_PaceActive

PACE = 0
VB = 1
VRP = 2
LRLONLY = 3
LRLANDPSYNC = 4

class VVI:
    '''VVI and VDD classes store the logic within the state diagram, and when to switch around'''
    def __init__(self, hardwareSystem=None):
        self.pState = VB
        if hardwareSystem is not None:
            self.sys = hardwareSystem
        else:
            self.sys = HardwareSystem()
        
        self.sys.setVBTimer()
        self.pastState = VB
        self.Mode = 'VVI'

    ### In this case, run() acts the same as the while loop in the example C code
    ### because run() runs on every frame 
    def run(self):
        if self.pState != self.pastState:
            self.pastState = self.pState
            print(self.pState)
        if self.pState == PACE:
            self.processPaceState()
        elif self.pState == VB:
            self.processVBState()
        elif self.pState == VRP:
            self.processVRPState()
        elif self.pState == LRLONLY:
            self.processLRLOnlyState()
        else:
            raise Exception("Invalid State")
        return self.sys.IO_PaceActive
        
    def processPaceState(self):
        if not self.sys.VPaceTimerActive:
            self.sys.VPaceOn()
            self.sys.setVPaceTimer()
            return
        if self.sys.VPaceTimer_expired():
            self.sys.VPaceOff()
            self.sys.clearVPaceTimer()
            self.pState = VB
            return
        return

    def processVBState(self):
        if not self.sys.VBTimerActive:
            self.sys.setVBTimer()
            return
        if self.sys.VBTimer_expired():
            self.sys.clearVBTimer()
            self.pState = VRP
            return
        return

    def processVRPState(self):
        if not self.sys.VRPTimerActive:
            self.sys.setVRPTimer()
            return
        if self.sys.VRPTimer_expired():
            self.sys.clearVRPTimer()
            self.pState = LRLONLY
            # self.sys.setLRLTimer()
            return
        return

    def processLRLOnlyState(self):
        if self.sys.LRL_timer_expired():
            self.sys.clearLRLTimer()
            self.sys.setLRLTimer()
            self.pState = PACE
            return
        if self.sys.Ventricular_Sensed():
            self.sys.clearLRLTimer()
            self.sys.setLRLTimer()
            self.pState = VB
            return
        return

class VDD(VVI):
    def __init__(self, hardwareSystem=None):
        self.pState = VB
        if hardwareSystem is not None:
            self.sys = hardwareSystem
        else:
            self.sys = HardwareSystem()
        
        self.sys.setVBTimer()
        self.pastState = VB
        self.Mode='VDD'

    def run(self):
        if self.pState != self.pastState:
            self.pastState = self.pState
            print(self.pState)
        if self.pState == PACE:
            self.processPaceState()
            return
        elif self.pState == VB:
            self.processVBState()
            return
        elif self.pState == VRP:
            self.processVRPState()
            return
        elif self.pState == LRLONLY:
            self.processLRLandPSyncState()
            return
        else:
            raise Exception("Invalid State")
        
    def processLRLandPSyncState(self):
        self.processLRLOnlyState()
        # If pacing due to LRL, skip the P Sync step
        if self.pState == PACE:
            self.sys.clearAVITimer()
            return
        self.processPSyncState()

    def processPSyncState(self):
        if self.sys.Atrial_Sensed() and not self.sys.AVITimerActive:
            self.sys.setAVITimer()

        if self.sys.AVITimerExpired():
            self.sys.clearAVITimer()
            self.sys.clearLRLTimer()
            self.sys.setLRLTimer()
            print("AVI Timer Expired")
            self.pState = PACE

        if self.sys.Ventricular_Sensed():
            self.sys.clearAVITimer() # processLRLOnlyState() will take care of the LRL timer
            self.pState = VB
            return


class HardwareSystem():
    '''Class that represents the physical systems and hardware of the pacemaker device
    If the pacing mode program is the software, this is the firmware/hardware/OS
    
    The pacing mode classes (VVI and VDD) store the logic for the state diagram, this class
        handles the steps that occur in each state'''
    def __init__(self, heart):
        # Save "Heart" object for IO
        self.heart=heart
        
        # Pacing voltage (in millivots)
        self.pacing_voltage = 0.5

        # Initialize parameters about the IO and interval timings
        self.LRLInt = 1000
        self.VPaceInt = 10
        self.VBInt = 100
        self.VRPInt = 200

        self.AVIInt = 200
        self.PVARP_Int = 250 # Post-ventricular atrial refractory period

        self.IO_VSensorActive = True
        self.IO_ASensorActive = True
        self.IO_PaceActive = False
        self.LRLTimerActive = False
        self.AVITimerActive = False

        self.LRLTimerEndValue = None
        self.VPaceTimerEndValue = None
        self.VBTimerEndValue = None    
        self.VRPTimerEndValue = None

        self.VPaceTimerActive = False
        self.VBTimerActive = False
        self.VRPTimerActive = False

    def current_time(self):
        '''Function that represents the hardware's onboard timing circuitry'''
        return time()*1000

    ##### LRL Functions: #####
    def LRL_timer_expired(self):
        if self.LRLTimerActive and self.current_time() >= self.LRLTimerEndValue:
            return True
        else:
            return False
        
    def clearLRLTimer(self):
        self.LRLTimerActive = False

    def setLRLTimer(self):
        print('LRL Timer Set')
        self.LRLTimerActive = True
        self.LRLTimerEndValue = self.current_time() + self.LRLInt

    ##### Atrioventricular Interval Functions (p wave sync): #####
    def AVITimerExpired(self):
        if self.AVITimerActive and self.current_time() >= self.AVITimerEndValue:
            return True
        else:
            return False

    def clearAVITimer(self):
        self.AVITimerActive = False

    def setAVITimer(self):
        self.AVITimerActive = True
        self.AVITimerEndValue = self.current_time() + self.AVIInt

    ##### Sensing Functions: #####
    def Ventricular_Sensed(self):
        # First, make sure IO Ventricular Sensor is on
        if self.IO_VSensorActive:
            if self.heart.rhythm.V_state == DEPOLARIZING:
                return True
        else:
            return False
        
    def Atrial_Sensed(self):
        # First, make sure IO Atrial Sensor is on
        if self.IO_ASensorActive:
            if self.heart.rhythm.A_state == DEPOLARIZING:
                return True
        else:
            return False

    ##### VPace Functions #####
    def VPaceOn(self):
        self.IO_ASensorActive = False
        self.IO_VSensorActive = False
        self.IO_PaceActive = True

    def VPaceOff(self):
        self.IO_PaceActive = False

    def setVPaceTimer(self):
        self.VPaceTimerActive = True
        self.VPaceTimerEndValue = self.current_time() + self.VPaceInt

    def VPaceTimer_expired(self):
        if self.VPaceTimerActive and self.current_time() >= self.VPaceTimerEndValue:
            return True
        else:
            return False
    
    def clearVPaceTimer(self):
        self.VPaceTimerActive = False
    
    ##### VB Functions: #####
    def setVBTimer(self):
        self.VBTimerActive = True
        self.IO_VSensorActive = False
        self.VBTimerEndValue = self.current_time() + self.VBInt

    def clearVBTimer(self):
        self.VBTimerActive = False
        self.IO_VSensorActive = True
        self.IO_ASensorActive = True

    def VBTimer_expired(self):
        if self.VBTimerActive and self.current_time() >= self.VBTimerEndValue:
            return True
        else:
            return False
    
    ##### VRP Functions #####
    def setVRPTimer(self):
        self.VRPTimerActive = True
        self.VRPTimerEndValue = self.current_time() + self.VRPInt

    def clearVRPTimer(self):
        self.VRPTimerActive = False
    
    def VRPTimer_expired(self):
        if self.VRPTimerActive and self.current_time() >= self.VRPTimerEndValue:
            return True
        else:
            return False


if __name__ == '__main__':
    from heart_activity import Heart
    heart = Heart()
