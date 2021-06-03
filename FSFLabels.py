

class FeatLevel:
    FIRST_LEVEL = 1
    HIGHER_LEVEL = 2

FeatLevelToStr = {
    FeatLevel.FIRST_LEVEL:"First-level analysis",
    FeatLevel.HIGHER_LEVEL:"Higher-level analysis"
}

class FeatAnalysis:
    FULL_ANALYSIS = 7
    PREPROCESSING = 1
    STATS = 2

FeatAnalysisToStr = {
    FeatAnalysis.STATS:"Stats",
    FeatAnalysis.PREPROCESSING:"Pre-processing",
    FeatAnalysis.FULL_ANALYSIS:"Full analysis"
}

class FeatSliceTiming:
    NONE = 0
    REGULAR_UP = 1
    REGULAR_DOWN = 2
    ORDER_FILE = 3
    TIMING_FILE = 4
    INTERLEAVED = 5
    Options = [NONE, REGULAR_UP, REGULAR_DOWN, ORDER_FILE, TIMING_FILE, INTERLEAVED]

class FeatPerfusion:
    FirstTimepointIsTag = 0
    FirstTimepointIsControl = 1
    Options = [FirstTimepointIsTag, FirstTimepointIsControl]

class FeatUnwarp:
    X_MINUS = "x-"
    X_PLUS = "x+"
    Y_MINUS = "y-"
    Y_PLUS = "y+"
    Z_MINUS = "z-"
    Z_PLUS = "z+"
    Directions = [X_PLUS,X_MINUS,Y_PLUS,Y_MINUS,Z_PLUS,Z_MINUS]

class FeatHigherLevelInput:
    FEAT_DIRS = 1
    COPE_IMAGES = 2

class RegistrationSearch:
    NO_SEARCH = 0
    NORMAL_SEARCH = 90
    FULL_SEARCH = 180
    Options = [NO_SEARCH, NORMAL_SEARCH, FULL_SEARCH]

class RegistrationDOF:
    DOF_3 = 3
    DOF_6 = 6
    DOF_7 = 7
    DOF_9 = 9
    DOF_12 = 12
    Options = [DOF_3,DOF_6,DOF_7,DOF_9,DOF_12]
