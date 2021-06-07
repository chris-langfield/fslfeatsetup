
class FeatEVShapes:
    Square = 0
    Sinusoid = 1
    Custom1EntryPerVolume = 2
    Custom3Column = 3
    Interaction = 4
    Empty = 10

class FeatHRFConvolution:
    NONE = 0
    Gaussian = 1
    Gamma = 2
    DoubleGamma = 3
    GammaBasis = 4
    SineBasis = 5
    FIRBasis = 6
    CustomBasis = 7

class Gamma:
    def __init__(self, phase=0, stdev=3, lag=6):
        self.phase = phase
        self.stdev = stdev
        self.lag = lag
        self.idx = 2

    def write(self, num):
        return f"set fmri(convolve_phase{num}) {self.phase}\n\nset fmri(gammasigma{num}) {self.stdev}\n\nset fmri(gammadelay{num})\n\n"


class DoubleGamma:
    def __init__(self, phase=0):
        self.phase = phase
        self.idx = 3
    def write(self, num):
        return f"set fmri(convolve_phase{num}) {self.phase}\n\n"

class AltDoubleGamma:
    def __init__(self, phase=0):
        self.phase = phase
        self.idx = 8
    def write(self, num):
        return f"set fmri(convolve_phase{num}) {self.phase}\n\n"


class Gaussian:
    def __init__(self, phase=0, sigma=2.8, peaklag = 5):
        self.phase = phase
        self.sigma = sigma
        self.peaklag = peaklag
        self.idx = 1

    def write(self, num):
        return f"set fmri(convolve_phase{num}) {self.phase}\n\nset fmri(gausssigma{num}) {self.sigma}\n\nset fmri(gaussdelay{num}) {self.peaklag}\n\n"


class FirstLevelEV:
    def __init__(self, name, filename, hrf, temporalDerivative=False, temporalFiltering=True, shape=FeatEVShapes.Custom3Column):
        self.name = name
        self.filename = filename
        self.hrf = hrf
        self.temporalDerivative = temporalDerivative
        self.temporalFiltering = temporalFiltering
        self.shape = shape

class HigherLevelEV:
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector

class Contrast:
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector