import numpy as np
from itertools import cycle
from queue import Queue

class heart:
    def __init__(self):
        self.rhythm = NSR()

    def set_rhythm(self, label):
        if label == 'NSR':
            self.rhythm = NSR()
        elif label == 'AFib':
            self.rhythm = AFib()

    def __iter__(self):
        return self.rhythm


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

if __name__ == '__main__':
    pass

