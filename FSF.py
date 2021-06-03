import os
import re
import subprocess
import fsl

# get $HOME

HOME = os.getenv("HOME")
print(HOME)

# get $FSLDIR
FSLDIR = os.getenv("FSLDIR")
if FSLDIR:
    print("$FSLDIR:",FSLDIR)
else:
    print("[!] Could not find environment variable $FSLDIR. Is FSL installed?")
    exit()

## get FEAT version
FEATLIB_PATH = os.path.join(FSLDIR, "src/feat5/featlib.tcl")
FEAT_VERSION = ""
with open(FEATLIB_PATH,"r") as FEATLIB:
    lines = [line for line in FEATLIB.readlines() if "set fmri(version)" in line]
for line in lines:
    try:
        float(line.split()[-1])
        FEAT_VERSION = line.split()[-1]
    except ValueError:
        continue

print("FEAT version:", FEAT_VERSION)

## get default settings
DEFAULT_SETTINGS_PATH = os.path.join(FSLDIR,"etc/fslconf/feat.tcl")
if not os.path.exists(DEFAULT_SETTINGS_PATH):
    print("Warning: default FEAT settings ($FSLDIR/etc/fslconf/feat.tcl does not exist. Defaults will not be loaded.")

class PyFSFError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'PyFSFError: ' + self.message
        else:
            return 'PyFSFError: '

class FeatLevel:
    FIRST_LEVEL = 1
    HIGHER_LEVEL = 2

FeatLevelToStr = {
    FeatLevel.FIRST_LEVEL:"First-level analysis",
    FeatLevel.HIGHER_LEVEL:"Higher-level analysis"
}

class FeatStages:
    FULL_ANALYSIS = 7
    PREPROCESSING = 1
    STATS = 2

FeatStagesToStr = {
    FeatStages.STATS:"Stats",
    FeatStages.PREPROCESSING:"Pre-processing",
    FeatStages.FULL_ANALYSIS:"Full analysis"
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

class FeatSettings:
    def __init__(self, LEVEL, ANALYSIS, defaultsFilename=DEFAULT_SETTINGS_PATH):

        self.settings = {}
        self.defaults = {}
        self.inputs = []
        self.altRefImages = []
        self.b0fieldMaps = []
        self.b0Magnitudes = []

        # must be set
        self.LEVEL = LEVEL
        self.ANALYSIS = ANALYSIS
        self.settings["level"] = LEVEL
        self.settings["analysis"] = ANALYSIS

        # FEAT version
        self.settings["version"] = FEAT_VERSION

        # get default settings
        if os.path.exists(defaultsFilename):
            with open(defaultsFilename) as defaults:
                lines = [line for line in defaults.readlines() if not line.startswith("#") and line.startswith("set")]
                for line in lines:
                    option = re.search('set fmri\((.*)\)', line).group(1)
                    value = line.split()[-1]
                    self.settings[option] = value
                    self.defaults[option] = value
        else:
            print("Warning: The defaults file specified (" + defaultsFilename + ") was not found. No settings were loaded.")

    def setLevel(self, LEVEL):
        if LEVEL in [1,2]:
            self.LEVEL = LEVEL
        else:
            print("Only first-level and higher-level analyses are allowed")
    def setAnalysis(self, ANALYSIS):
        if ANALYSIS in [1,2,7]:
            self.ANALYSIS = ANALYSIS
        else:
            print("Only full analysis, preprocessing, and stats are allowed")

    def printSettings(self):
        for option in self.settings:
            print(option,'--',self.settings[option])


class DataOptions:
    def __init__(self, myFeatSettings):
        self.parent = myFeatSettings
        # default
        if "paradigm_hp" in self.parent.defaults:
            self.DEFAULT_HIGHPASS_CUTOFF = self.parent.defaults["paradigm_hp"]
        if "ndelete" in self.parent.defaults:
            self.DEFAULT_DELETE_VOLUMES = self.parent.defaults["ndelete"]

    def Configure(self, outputDirectory, inputPaths, totalVolumes=-1, deleteVolumes = -1, tr =-1, highPassCutoff = -1, higherLevelInput = FeatHigherLevelInput.COPE_IMAGES):
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:

            if not tr == -1:
                print("TR specified by user. Will not get TR from input image")
                self.parent.settings["tr"] = tr
            else:
                tr = subprocess.getoutput([FSLDIR + "/bin/fslval " + inputPaths[0] + " pixdim4"])
                self.parent.settings["tr"] = float(tr.replace("\n","").strip())
                print("TR is ", tr.replace("\n","").strip())
            if not totalVolumes == -1:
                print("Number of volumes specified by user. Will not get TR from input image")
                self.parent.settings["npts"] = totalVolumes
            else:
                totalVolumes = subprocess.getoutput([FSLDIR + "/bin/fslnvols " + inputPaths[0]])
                self.parent.settings["npts"] = int(totalVolumes.replace("\n","").strip())
                print("Total volumes are", totalVolumes.replace("\n","").strip())

            if deleteVolumes == -1:
                if hasattr(self, 'DEFAULT_DELETE_VOLUMES'):
                    deleteVolumes = self.DEFAULT_DELETE_VOLUMES
                else:
                    deleteVolumes = 0
            self.parent.settings["ndelete"] = deleteVolumes

            if highPassCutoff == -1:
                if hasattr(self, 'DEFAULT_HIGHPASS_CUTOFF'):
                    highPassCutoff = self.DEFAULT_HIGHPASS_CUTOFF
                else:
                    highPassCutoff = 100
            self.parent.settings["paradigm_hp"] = highPassCutoff

        elif self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            self.parent.settings["inputtype"] = higherLevelInput
            self.parent.settings["npts"] = len(inputPaths)

        self.parent.settings["outputdir"] = outputDirectory
        self.parent.settings["multiple"] = len(inputPaths)

        # input paths

        for i in range(len(inputPaths)):
            self.parent.inputs.append(inputPaths[i])


        ## voxel size
        dim1 = int(
            subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
        dim2 = int(
            subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
        dim3 = int(
            subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
        dim4 = int(
            subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())

        totalVoxels = dim1 * dim2 * dim3 * dim4
        self.parent.settings["totalVoxels"] = totalVoxels



    def printSettings(self):
        print("Data Settings: " + self.parent.settings["outputdir"])
        print(FeatLevelToStr[self.parent.LEVEL], "|", FeatStagesToStr[self.parent.ANALYSIS])
        print("--------------")
        print("Number of inputs:", self.parent.settings["multiple"])
        print("Total volumes:", self.parent.settings["npts"])
        print("TR:", self.parent.settings["tr"])
        print("High pass filter cutoff:", self.parent.settings["paradigm_hp"])
        if self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            print("Input type: (1=lower level feat directories, 2=lower level cope images)", self.parent.settings["inputtype"])
        print("Inputs: ")
        for i in range(len(self.parent.inputs)):
            print("\t", i+1, self.parent.inputs[i])


class MiscOptions:
    def __init__(self, myFeatOptions):
        self.parent = myFeatOptions
        # default
        if "brain_thresh" in self.parent.defaults:
            self.DEFAULT_BRAIN_THRESH = int(self.parent.defaults["brain_thresh"])
        if "noise" in self.parent.defaults:
            self.DEFAULT_NOISE = float(self.parent.defaults["noise"])
        if "noisear" in self.parent.defaults:
            self.DEFAULT_SMOOTHNESS = float(self.parent.defaults["noisear"])
        if "critical_z" in self.parent.defaults:
            self.DEFAULT_CRITICAL_Z = float(self.parent.defaults["critical_z"])
        if "sscleanup" in self.parent.defaults:
            if int(self.parent.defaults["sscleanup"]) == 1:
                self.DEFAULT_CLEANUP_FIRSTLEVEL_YN = True
            else:
                self.DEFAULT_CLEANUP_FIRSTLEVEL_YN = False
        if "newdir_yn" in self.parent.defaults:
            if int(self.parent.defaults["newdir_yn"]) == 1:
                self.DEFAULT_OVERWRITE_POSTSTATS = True
            else:
                self.DEFAULT_OVERWRITE_POSTSTATS = False

    def Configure(self, brainThreshold=-1, noiseLevel=-1, temporalSmoothness=-1, zThreshold=-1, cleanupFirstLevel=None, overwriteOriginalPostStats = None, estimateNoiseFromData=False):
        if brainThreshold == -1:
            if hasattr(self, 'DEFAULT_BRAIN_THRESH'):
                brainThreshold = self.DEFAULT_BRAIN_THRESH
            else:
                brainThreshold = 10
        self.parent.settings["brain_thresh"] = brainThreshold

        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:

            if noiseLevel == -1:
                if hasattr(self, 'DEFAULT_NOISE'):
                    noiseLevel = self.DEFAULT_NOISE
                else:
                    noiseLevel = 0.66
            self.parent.settings["noise"] = noiseLevel

            if temporalSmoothness == -1:
                if hasattr(self, 'DEFAULT_SMOOOTHNESS'):
                    temporalSmoothness = self.DEFAULT_SMOOTHNESS
                else:
                    temporalSmoothness = 0.34
            self.parent.settings["noisear"] = temporalSmoothness

            if zThreshold == -1:
                if hasattr(self, 'DEFAULT_CRITICAL_Z'):
                    zThreshold = self.DEFAULT_CRITICAL_Z
                else:
                    zThreshold = 5.3
            self.parent.settings["critical_z"] = zThreshold

        if self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            if cleanupFirstLevel is None:
                if hasattr(self, 'DEFAULT_CLEANUP_FIRSTLEVEL_YN'):
                    cleanupFirstLevel = self.DEFAULT_CLEANUP_FIRSTLEVEL_YN
                else:
                    cleanupFirstLevel = False
            self.parent.settings["sscleanup"] = int(cleanupFirstLevel)

            if overwriteOriginalPostStats is None:
                if hasattr(self, 'DEFAULT_OVERWRITE_POSTSTATS'):
                    overwriteOriginalPostStats = self.DEFAULT_OVERWRITE_POSTSTATS
                else:
                    overwriteOriginalPostStats = False
            self.parent.settings["newdir_yn"] = overwriteOriginalPostStats



    def printSettings(self):
        print("Misc Settings: " + self.parent.settings["outputdir"])
        print(FeatLevelToStr[self.parent.LEVEL], "|", FeatStagesToStr[self.parent.ANALYSIS])
        print("--------------")
        print("Brain/background threshold:", self.parent.settings["brain_thresh"])
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:
            print("Noise level %:", self.parent.settings["noise"])
            print("Temporal smoothness:", self.parent.settings["noisear"])
            print("Z-threshold:", self.parent.settings["critical_z"])
        if self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            print("Cleanup first level standard-space images", self.parent.settings["sscleanup"])



class PreStatsOptions:
    def __init__(self, myFeatSettings):
        self.parent = myFeatSettings
        self.CONFIGURED = False
        # default
        if "dwell" in self.parent.defaults:
            self.DEFAULT_EPI_DWELL = float(self.parent.defaults["dwell"])
        if "te" in self.parent.defaults:
            self.DEFAULT_EPI_TE = float(self.parent.defaults["te"])
        if "signallossthresh" in self.parent.defaults:
            self.DEFAULT_SIGNAL_LOSS = float(self.parent.defaults["signallossthresh"])
        if "smooth" in self.parent.defaults:
            self.DEFAULT_SMOOOTH = float(self.parent.defaults["smooth"])
        if "unwarp_dir" in self.parent.defaults:
            if self.parent.defaults["unwarp_dir"] in FeatUnwarp.Directions:
                self.DEFAULT_UNWARP_DIR = self.parent.defaults["unwarp_dir"]
        if "st" in self.parent.defaults:
            if int(self.parent.defaults["st"]) in FeatSliceTiming.Options:
                self.DEFAULT_SLICE_TIMING = int(self.parent.defaults["st"])
        if "mc" in self.parent.defaults:
            if int(self.parent.defaults["mc"]) == 1:
                self.DEFAULT_MCFLIRT = True
            else:
                self.DEFAULT_MCFLIRT = False
        if "regunwarp_yn" in self.parent.defaults:
            if int(self.parent.defaults["regunwarp_yn"]) == 1:
                self.DEFAULT_B0_UNWARP = True
            else:
                self.DEFAULT_B0_UNWARP = False
        if "alternateReference_yn" in self.parent.defaults:
            if int(self.parent.defaults["alternateReference_yn"]) == 1:
                self.DEFAULT_ALT_REF_IMG = True
            else:
                self.DEFAULT_ALT_REF_IMG = False
        if "bet_yn" in self.parent.defaults:
            if int(self.parent.defaults["bet_yn"]) == 1:
                self.DEFAULT_BET = True
            else:
                self.DEFAULT_BET = False
        if "norm_yn" in self.parent.defaults:
            if int(self.parent.defaults["norm_yn"]) == 1:
                self.DEFAULT_NORM = True
            else:
                self.DEFAULT_NORM = False
        if "perfsub_yn" in self.parent.defaults:
            if int(self.parent.defaults["perfsub_yn"]) == 1:
                self.DEFAULT_PERFSUB = True
            else:
                self.DEFAULT_PERFSUB = False
        if "tagfirst" in self.parent.defaults:
            if int(self.parent.defaults["tagfirst"]) in FeatPerfusion.Options:
                self.DEFAULT_PERF_TAGFIRST = int(self.parent.defaults["tagfirst"])
        if "temphp_yn" in self.parent.defaults:
            if int(self.parent.defaults["temphp_yn"]) == 1:
                self.DEFAULT_TEMPORAL_HIGHPASS = True
            else:
                self.DEFAULT_TEMPORAL_HIGHPASS = False
        if "templp_yn" in self.parent.defaults:
            if int(self.parent.defaults["templp_yn"]) == 1:
                self.DEFAULT_TEMPORAL_LOWPASS = True
            else:
                self.DEFAULT_TEMPORAL_LOWPASS = False
        if "melodic_yn" in self.parent.defaults:
            if int(self.parent.defaults["melodic_yn"]) == 1:
                self.DEFAULT_MELODIC = True
            else:
                self.DEFAULT_MELODIC = False

    def Configure(self,
                  mcflirt = None, # bool
                  b0_unwarp = None, # bool
                  melodic = None, # bool
                  sliceTiming = None, # int
                  sliceTimingFile = None, # filepath
                  bet = None, # bool
                  spatialSmoothing = -1.0, # float
                  intensityNormalization = None, # bool
                  perfusionSubtraction = None, # bool
                  perfusionTagControlOrder = -1, # int
                  highPassTemporalFilter = None, # bool
                  lowPassTemporalFilter = None, # bool
                  usingAlternateReferenceImage = None, # bool
                  alternateReferenceImages = None): ## list of paths

        if mcflirt is None:
            if hasattr(self, 'DEFAULT_MCFLIRT'):
                mcflirt = self.DEFAULT_MCFLIRT
            else:
                mcflirt = 0
        self.parent.settings["mc"] = mcflirt

        if b0_unwarp is None:
            if hasattr(self, 'DEFAULT_B0_UNWARP'):
                b0_unwarp = self.DEFAULT_B0_UNWARP
            else:
                b0_unwarp = False
        self.parent.settings["regunwarp_yn"] = b0_unwarp

        if melodic is None:
            if hasattr(self, 'DEFAULT_MELODIC'):
                melodic = self.DEFAULT_MELODIC
            else:
                melodic = False
        self.parent.settings["melodic_yn"] = melodic

        if sliceTiming is None:
            if hasattr(self, 'DEFAULT_SLICE_TIMING'):
                sliceTiming = self.DEFAULT_SLICE_TIMING
            else:
                sliceTiming = FeatSliceTiming.NONE
        self.parent.settings["st"] = sliceTiming

        if bet is None:
            if hasattr(self, 'DEFAULT_BET'):
                bet = self.DEFAULT_BET
            else:
                bet = False
        self.parent.settings["bet_yn"] = bet

        if spatialSmoothing is None:
            if hasattr(self, 'DEFAULT_SMOOTH'):
                spatialSmoothing = self.DEFAULT_SMOOTH
            else:
                spatialSmoothing = 5.0
        self.parent.settings["smooth"] = spatialSmoothing

        if sliceTimingFile is None:
            if not self.parent.settings["st"] not in [FeatSliceTiming.NONE, FeatSliceTiming.INTERLEAVED, FeatSliceTiming.REGULAR_DOWN, FeatSliceTiming.REGULAR_UP]:
                print("Error: Slice timing or slice order file is required")
                return
        else:
            self.parent.settings["st_file"] = sliceTimingFile

        if intensityNormalization is None:
            if hasattr(self, 'DEFAULT_NORM'):
                intensityNormalization = self.DEFAULT_NORM
            else:
                intensityNormalization = False
        self.parent.settings["norm_yn"] = intensityNormalization

        if perfusionSubtraction is None:
            if hasattr(self, 'DEFAULT_PERFSUB'):
                perfusionSubtraction = self.DEFAULT_PERFSUB
            else:
                perfusionSubtraction = False
        self.parent.settings["perfsub_yn"] = perfusionSubtraction

        if perfusionTagControlOrder is None:
            if hasattr(self, 'DEFAULT_PERF_TAGFIRST'):
                perfusionTagControlOrder = self.DEFAULT_PERF_TAGFIRST
            else:
                perfusionTagControlOrder = FeatPerfusion.FirstTimepointIsTag
        self.parent.settings["tagfirst"] = perfusionTagControlOrder

        if highPassTemporalFilter is None:
            if hasattr(self, 'DEFAULT_TEMPORAL_HIGHPASS'):
                highPassTemporalFilter = self.DEFAULT_TEMPORAL_HIGHPASS
            else:
                highPassTemporalFilter = False
        self.parent.settings["temphp_yn"] = highPassTemporalFilter

        if lowPassTemporalFilter is None:
            if hasattr(self, 'DEFAULT_TEMPORAL_LOWPASS'):
                lowPassTemporalFilter = self.DEFAULT_TEMPORAL_LOWPASS
            else:
                loowPassTemporalFilter = False
        self.parent.settings["templp_yn"] = lowPassTemporalFilter

        if usingAlternateReferenceImage is None:
            if hasattr(self, 'DEFAULT_ALT_REF_IMG'):
                usingAlternateReferenceImage = self.DEFAULT_ALT_REF_IMG
            else:
                usingAlternateReferenceImage = False
        self.parent.settings["alternativeReference_yn"] = usingAlternateReferenceImage

        if alternateReferenceImages is None:
            if usingAlternateReferenceImage:
                print("Error: must specify at least one alternate reference image")
        else:
            numAltImages = len(alternateReferenceImages)
            # use up to the first 3 reference images provided
            for i in range(0, min(3, numAltImages)):
                self.parent.altRefImages.append(alternateReferenceImages[i])

        self.CONFIGURED = True

    def Unwarping(self,
                  fieldmapImages, # list of paths
                  fieldmapMagnitudeImages, # list of magnitudes
                  epiDwell = None, # float
                  epiTE = None, # float
                  unwarpDir = None, # string
                  signalLoss = None, # int
                  ):
        if not self.CONFIGURED:
            print("Error: The Pre-Stats options have not been configured. Use PreStatsOptions.Configure()")
            return
        if fieldmapImages in [[], None]:
            print("Error: specify fieldmap images")
            return
        if fieldmapMagnitudeImages in [[], None]:
            print("Error: specify fieldmap magnitude images")
            return

        numFieldMapImages = len(fieldmapImages)
        for i in range(0, min(3, numFieldMapImages)):
            self.parent.b0fieldMaps.append(fieldmapImages[i])
        numMagnitudeImages = len(fieldmapMagnitudeImages)
        for i in range(0, min(3, numMagnitudeImages)):
            self.parent.b0Magnitudes.append(fieldmapMagnitudeImages[i])

        if epiDwell is None:
            if hasattr(self, 'DEFAULT_EPI_DWELL'):
                epiDwell = self.DEFAULT_EPI_DWELL
            else:
                epiDwell = 0.0
        self.parent.settings["dwell"] = epiDwell

        if epiTE is None:
            if hasattr(self, 'DEFAULT_EPI_TE'):
                epiTE = self.DEFAULT_EPI_TE
            else:
                epiTE = 0.0
        self.parent.settings["te"] = epiTE

        if signalLoss is None:
            if hasattr(self,'DEFAULT_SIGNAL_LOSS'):
                signalLoss = self.DEFAULT_SIGNAL_LOSS
            else:
                signalLoss = 10
        self.parent.settings["signallossthresh"] = signalLoss

        if unwarpDir is None:
            if hasattr(self, 'DEFAULT_UNWARP_DIR'):
                unwarpDir = self.DEFAULT_UNWARP_DIR
            else:
                unwarpDir = FeatUnwarp.Y_MINUS
        self.parent.settings["unwarp_dir"] = unwarpDir