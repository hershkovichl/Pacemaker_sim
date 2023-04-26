class heart:
    def __init__(self):
        self.state = 'NSR'


class NSR(heart):
    def __init__(self):
        pass

    def p_wave(self):
        # p wave sequence
        pass


class AFib(heart):
    def __init__(self):
        pass
    def p_wave(self):
        # Random noise + sin wave
        pass

