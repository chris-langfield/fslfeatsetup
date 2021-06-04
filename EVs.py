
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


class DoubleGamma:
    def __init__(self, phase=0):
        self.phase = phase

class Gaussian:
    def __init__(self, phase=0, sigma=2.8, peaklag = 5):
        self.phase = phase
        self.sigma = sigma
        self.peaklag = peaklag

class EV:
    def __init__(self, name, filename, hrf, temporalDerivative=False, temporalFiltering=True, shape=FeatEVShapes.Custom3Column):
        self.name = name
        self.filename = filename
        self.hrf = hrf
        self.temporalDerivative = temporalDerivative
        self.temporalFiltering = temporalFiltering