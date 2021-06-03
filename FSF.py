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

class FeatHigherLevelInput:
    FEAT_DIRS = 1
    COPE_IMAGES = 2

class FeatSettings:
    def __init__(self, LEVEL, ANALYSIS, defaultsFilename=DEFAULT_SETTINGS_PATH):

        self.settings = {}
        self.inputs = []

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

    def Configure(self, outputDirectory, inputPaths, totalVolumes=-1, deleteVolumes = -1, tr =-1, highPassCutoff = 60, higherLevelInput = FeatHigherLevelInput.COPE_IMAGES):
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:
            if not tr == -1:
                print("TR specified by user. Will not get TR from input image")
            else:
                tr = subprocess.getoutput([FSLDIR + "/bin/fslval " + inputPaths[0] + " pixdim4"])
                self.parent.settings["tr"] = float(tr.replace("\n","").strip())
                print("TR is ", tr.replace("\n","").strip())
            if not totalVolumes == -1:
                print("Number of volumes specified by user. Will not get TR from input image")
            else:
                totalVolumes = subprocess.getoutput([FSLDIR + "/bin/fslnvols " + inputPaths[0]])
                self.parent.settings["npts"] = int(totalVolumes.replace("\n","").strip())
                print("Total volumes are", totalVolumes.replace("\n","").strip())
            if not deleteVolumes == -1:
                self.parent.settings["ndelete"] = deleteVolumes
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
        dim1 = int(subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
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

    def Configure(self, brainThreshold=10, noiseLevel=0.66, temporalSmoothness=0.34, zThreshold=5.3, cleanupFirstLevel=False, estimateNoiseFromData=False):
        self.parent.settings["brain_thresh"] = brainThreshold
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:
            self.parent.settings["noise"] = noiseLevel
            self.parent.settings["noisear"] = temporalSmoothness
            self.parent.settings["critical_z"] = zThreshold
        if self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            self.parent.settings["sscleanup"] = int(cleanupFirstLevel)

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
    def __init__(self):
        pass

