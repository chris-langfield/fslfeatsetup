
class FeatEVShapes:
    """
    Enum specifying all the options for a first-level EV. Used for the shape kwarg in the constructor of the FirstLevelEV class
    Only Custom3Column currently enabled
    """
    Square = 0
    Sinusoid = 1
    Custom1EntryPerVolume = 2
    Custom3Column = 3
    Interaction = 4
    Empty = 10

class FeatHRFConvolution:
    """
    Enum specifying the types of HRF convolutions for a first level EV. Possibly unneeded.
    """
    NONE = 0
    Gaussian = 1
    Gamma = 2
    DoubleGamma = 3
    GammaBasis = 4
    SineBasis = 5
    FIRBasis = 6
    CustomBasis = 7

class Gamma:
    """
    Object representing a Gamma convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.
    """
    def __init__(self, phase=0, stdev=3, lag=6):
        self.phase = phase
        self.stdev = stdev
        self.lag = lag
        self.idx = 2

    def write(self, num):
        return f"# Convolve phase (EV {num})\nset fmri(convolve_phase{num}) {self.phase}\n\n# Gamma standard deviation (EV {num})\nset fmri(gammasigma{num}) {self.stdev}\n\n# Gamma delay (EV {num})\nset fmri(gammadelay{num}) {self.lag}\n\n"


class DoubleGamma:
    """
    Object representing a Double Gamma convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.
    """
    def __init__(self, phase=0):
        self.phase = phase
        self.idx = 3
    def write(self, num):
        return f"# Convolve phase (EV {num})\nset fmri(convolve_phase{num}) {self.phase}\n\n"

class AltDoubleGamma:
    """
    Object representing an Alternate Double Gamma convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.
    """
    def __init__(self, phase=0):
        self.phase = phase
        self.idx = 8
    def write(self, num):
        return f"# Convolve phase (EV {num})\nset fmri(convolve_phase{num}) {self.phase}\n\n"


class Gaussian:
    """
    Object representing a Gaussian convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.
    """
    def __init__(self, phase=0, sigma=2.8, peaklag = 5):
        self.phase = phase
        self.sigma = sigma
        self.peaklag = peaklag
        self.idx = 1

    def write(self, num):
        return f"# Convolve phase (EV {num})\nset fmri(convolve_phase{num}) {self.phase}\n\nset fmri(gausssigma{num}) {self.sigma}\n\nset fmri(gaussdelay{num}) {self.peaklag}\n\n"


class FirstLevelEV:
    """
    Object representing a first level EV. Will be refactored.
    """
    def __init__(self, name, filename, hrf, temporalDerivative=False, temporalFiltering=True, shape=FeatEVShapes.Custom3Column):
        self.name = name
        self.filename = filename
        self.hrf = hrf
        self.temporalDerivative = temporalDerivative
        self.temporalFiltering = temporalFiltering
        self.shape = shape

class HigherLevelEV:
    """
    Object representing a higher level EV
    """
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector

class Contrast:
    """
    Object representing a contrast
    """
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector