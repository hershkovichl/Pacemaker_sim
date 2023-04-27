import numpy as np
from itertools import cycle
from queue import Queue

class heart:
    def __init__(self):
        self.rhythm = NSR()
        self.rhythmName = 'NSR'

    def set_rhythm(self, label):
        self.rhythmName = label
        if label == 'NSR':
            self.rhythm = NSR()
        elif label == 'AFib':
            self.rhythm = AFib()
        elif label == 'AV_Block':
            self.rhythm = AV_Block()
        elif label == 'AFib_AV_Block':
            self.rhythm = AFib_AV_Block()

    def __iter__(self):
        return self.rhythm
    
    def __next__(self):
        # Pass state to pacemaker, then pacemaker decides
        return next(self.rhythm)


class NSR:
    def __init__(self, scale=1):
        self.scale = scale
        self.cycle = cycle([self.p_wave, self.PR_int, self.QRS, self.QT_int, self.t_wave, self.TP_int])
        self.queue = []
        self.i = 0

    def p_wave(self, scale=1):
        t = np.linspace(0,np.pi, 10 * scale * self.scale)
        return 0.08* np.sin(t)
    
    def PR_int(self, scale=1):
        return np.zeros(5*scale*self.scale)
    
    def QRS(self, scale=1):
        d1 = np.linspace(0,-0.1, 2*scale*self.scale)
        up1 = np.linspace(-0.1, 0.6, 3*scale*self.scale)[1:]
        d2 = np.linspace(0.6, -0.3, 3*scale*self.scale)[1:]
        up2 = np.linspace(-0.3, 0, 2*scale*self.scale)[1:]
        return np.concatenate([d1,up1,d2,up2])
        
    def QT_int(self, scale=1):
        return np.zeros(8*scale*self.scale)
    
    def t_wave(self, scale=1):
        t = np.linspace(0,np.pi, 15 * scale * self.scale)
        return 0.16*np.sin(t)
    
    def TP_int(self, scale=1):
        return np.zeros(15*scale*self.scale)

    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self.queue) == self.i:
            nextfunc = next(self.cycle)
            self.queue = nextfunc()
            self.i = 0
        retVal = self.queue[self.i]
        self.i += 1
        return retVal + 0.01 * np.random.randn()

class AFib:
    def __init__(self, scale=1):
        self.scale = scale
        self.cycle = cycle([self.PQ_int, self.QRS, self.QT_int, self.t_wave])
        self.queue = []
        self.i = 0

        self.fibrillation_magnitude = 0.03
    
    def PQ_int(self, scale=1):
        randomness = np.random.randint(low=1, high=15)
        t = np.zeros(randomness * scale * self.scale)
        return t
    
    def QRS(self, scale=1):
        d1 = np.linspace(0,-0.1, 2*scale*self.scale)
        up1 = np.linspace(-0.1, 0.6, 3*scale*self.scale)[1:]
        d2 = np.linspace(0.6, -0.3, 3*scale*self.scale)[1:]
        up2 = np.linspace(-0.3, 0, 2*scale*self.scale)[1:]
        return np.concatenate([d1,up1,d2,up2])
        
    def QT_int(self, scale=1):
        return np.zeros(8*scale*self.scale)
    
    def t_wave(self, scale=1):
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
    
class AV_Block:
    '''Two iterators, take the max of them'''
    def __init__(self, scale = 1):
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
    def __init__(self, scale=1):
        super().__init__(scale)

    def PQ_int(self, scale=1):
        t = np.zeros(47 * scale * self.scale)
        return t

if __name__ == '__main__':
    pass

