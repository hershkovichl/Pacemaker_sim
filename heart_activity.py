import numpy as np
from itertools import cycle
from queue import Queue

class Heart:
    def __init__(self):
        self.rhythm = NSR(self)
        self.rhythmName = 'NSR'
        self.pacemaker = None
        self.newrhythm = False
        self.newrhythmlabel = ''

    # TODO: make a "self.newrhythm" and await TPSEG to switch (in __next__)
    def set_rhythm(self, label):
        self.newrhythmlabel = label
        self.newrhythm = True
    
    def _set_rhythm(self):
        label = self.newrhythmlabel
        self.rhythmName = self.newrhythmlabel
        if label == 'NSR':
            self.rhythm = NSR(self)
        elif label == 'AFib':
            self.rhythm = AFib(self)
        elif label == 'AV_Block':
            self.rhythm = AV_Block(self)
        elif label == 'AFib_AV_Block':
            self.rhythm = AFib_AV_Block(self)

    def set_pacemaker(self, pacemaker):
        self.pacemaker = pacemaker

    def remove_pacemaker(self):
        self.pacemaker = None

    def __iter__(self):
        return self.rhythm
    
    def __next__(self):
        # Pass state to pacemaker, then pacemaker decides
        if self.newrhythm:
            if self.rhythm.ecg_state == PWAVE:
                self._set_rhythm()
                
        if self.pacemaker is not None:
            V_pace = self.pacemaker.run()
        return next(self.rhythm)

# Defined states for Atria and Ventricles
POLARIZED = 0
DEPOLARIZING = 1
REFRACTORY = 2
REPOLARIZING = 3
FIBRILLATION = 4

# Defined unified state for the ECG
TPSEG = 0
PWAVE = 1
PQSEG = 2
QRST = 3
AFIB = 4

class Rhythm:
    def __init__(self, heart):
        self.heart = heart
        self.A_state = POLARIZED
        self.V_state = POLARIZED
        self.ecg_state = TPSEG

class NSR(Rhythm):
    def __init__(self, heart, scale=1):
        super().__init__(heart=heart)
        self.scale = scale
        self.cycle = cycle([self.p_wave, self.PR_int, self.QRS, self.QT_int, self.t_wave, self.TP_int])
        self.queue = []
        self.currentFunc = ''
        self.i = 0

    def p_wave(self, scale=1):
        self.ecg_state = PWAVE
        self.A_state = DEPOLARIZING
        t = np.linspace(0,np.pi, 10 * scale * self.scale)
        return 0.08* np.sin(t)
    
    def PR_int(self, scale=1):
        self.A_state = REFRACTORY
        self.ecg_state = PQSEG
        return np.zeros(5*scale*self.scale)
    
    def QRS(self, scale=1):
        self.A_state = REPOLARIZING
        self.ecg_state = QRST
        self.V_state = DEPOLARIZING
        d1 = np.linspace(0,-0.1, 2*scale*self.scale)
        up1 = np.linspace(-0.1, 0.6, 3*scale*self.scale)[1:]
        d2 = np.linspace(0.6, -0.3, 3*scale*self.scale)[1:]
        up2 = np.linspace(-0.3, 0, 2*scale*self.scale)[1:]
        return np.concatenate([d1,up1,d2,up2])
        
    def QT_int(self, scale=1):
        self.A_state = POLARIZED
        self.V_state = REFRACTORY
        return np.zeros(8*scale*self.scale)
    
    def t_wave(self, scale=1):
        self.V_state = REPOLARIZING
        t = np.linspace(0,np.pi, 15 * scale * self.scale)
        return 0.16*np.sin(t)
    
    def TP_int(self, scale=1):
        self.V_state = POLARIZED
        self.ecg_state = TPSEG
        return np.zeros(15*scale*self.scale)

    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.queue) == self.i:
            nextfunc = next(self.cycle)
            self.queue = nextfunc()
            self.currentFunc = nextfunc.__name__
            self.i = 0
        retVal = self.queue[self.i]
        self.i += 1
        return retVal + 0.01 * np.random.randn()

class AFib(Rhythm):
    def __init__(self, heart, scale=1):
        super().__init__(heart=heart)
        self.scale = scale
        self.cycle = cycle([self.PQ_int, self.QRS, self.QT_int, self.t_wave])
        self.queue = []
        self.i = 0

        self.fibrillation_magnitude = 0.03
    
    def PQ_int(self, scale=1):
        self.V_state = POLARIZED
        self.ecg_state = AFIB
        self.A_state = FIBRILLATION
        randomness = np.random.randint(low=1, high=15)
        t = np.zeros(randomness * scale * self.scale)
        return t
    
    def QRS(self, scale=1):
        self.V_state = DEPOLARIZING
        self.ecg_state = QRST
        d1 = np.linspace(0,-0.1, 2*scale*self.scale)
        up1 = np.linspace(-0.1, 0.6, 3*scale*self.scale)[1:]
        d2 = np.linspace(0.6, -0.3, 3*scale*self.scale)[1:]
        up2 = np.linspace(-0.3, 0, 2*scale*self.scale)[1:]
        return np.concatenate([d1,up1,d2,up2])
        
    def QT_int(self, scale=1):
        self.V_state = REFRACTORY
        return np.zeros(8*scale*self.scale)
    
    def t_wave(self, scale=1):
        self.V_state = REPOLARIZING
        t = np.linspace(0,np.pi, 15 * scale * self.scale)
        return 0.16*np.sin(t)

    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.queue) == self.i:
            nextfunc = next(self.cycle)
            self.queue = nextfunc()
            self.i = 0
        retVal = self.queue[self.i]
        self.i += 1
        return retVal + self.fibrillation_magnitude * np.random.randn()
    
class AV_Block(Rhythm):
    '''Two iterators, take the max of them'''
    def __init__(self, heart, scale = 1):
        super().__init__(heart=heart)
        self.scale = scale
        self.SA_cycle = cycle([self.p_wave, self.SA_refractory])
        self.AV_cycle = cycle([self.QRST, self.AV_refractory])
        self.SA_queue = []
        self.AV_queue = []
        self.SA_i = 0
        self.AV_i = 0

    def QRST(self, scale=1):
        d1 = np.linspace(0,-0.1, 2*scale*self.scale)
        up1 = np.linspace(-0.1, 0.6, 3*scale*self.scale)[1:]
        d2 = np.linspace(0.6, -0.3, 3*scale*self.scale)[1:]
        up2 = np.linspace(-0.3, 0, 2*scale*self.scale)[1:]

        qt_int = np.zeros(8*scale*self.scale)
        t_wave = 0.16*np.sin(np.linspace(0,np.pi, 15 * scale * self.scale))
        return np.concatenate([d1,up1,d2,up2, qt_int, t_wave])

    def p_wave(self, scale=1):
        t = np.linspace(0,np.pi, 10 * scale * self.scale)
        return 0.08* np.sin(t)
    
    def SA_refractory(self, scale = 1):
        return np.zeros(40 * scale)
    
    def AV_refractory(self, scale = 1):
        return np.zeros(47 * scale)

    def __next__(self):
        if len(self.SA_queue) == self.SA_i:
            nextfunc = next(self.SA_cycle)
            self.SA_queue = nextfunc()
            self.SA_i = 0
        if len(self.AV_queue) == self.AV_i:
            nextfunc = next(self.AV_cycle)
            self.AV_queue = nextfunc()
            self.AV_i = 0
        nextSA = self.SA_queue[self.SA_i]
        nextAV= self.AV_queue[self.AV_i]
        retVal = max(nextSA, nextAV)
        self.SA_i += 1
        self.AV_i += 1
        return retVal + 0.01 * np.random.randn()


class AFib_AV_Block(AFib):
    def __init__(self, heart, scale=1):
        super().__init__(heart=heart, scale=scale)

    def PQ_int(self, scale=1):
        self.V_state = POLARIZED
        self.ecg_state = AFIB
        self.A_state = FIBRILLATION
        t = np.zeros(47 * scale * self.scale)
        return t

if __name__ == '__main__':
    pass

