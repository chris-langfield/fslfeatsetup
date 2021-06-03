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

class FeatStages:
    FULL_ANALYSIS = 1
    PREPROCESSING = 2
    STATS = 3

class FeatHigherLevelInput:
    FEAT_DIRS = 1
    COPE_IMAGES = 2

class FeatSettings:
    def __init__(self, defaultsFilename=DEFAULT_SETTINGS_PATH, LEVEL, ANALYSIS):
        # must be set
        self.LEVEL = LEVEL
        self.ANALYSIS = ANALYSIS

        self.settings = {}

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
        if ANALYSIS in [1,2,3]:
            self.ANALYSIS = ANALYSIS
        else:
            print("Only full analysis, preprocessing, and stats are allowed")




    def printSettings(self):
        for option in self.settings:
            print(option,'--',self.settings[option])


class DataOptions:
    def __init__(self, myFeatSettings):
        self.parent = myFeatSettings

    def Configure(self, outputDirectory, numInputs, inputPaths, totalVolumes=-1, deleteVolumes = -1, tr =-1, highPassCutoff = 60, higherLevelInput = FeatHigherLevelInput.FEAT_DIRS):
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:
            if not tr == -1:
                print("TR specified by user. Will not get TR from input image")
            else:
                tr = subprocess.getoutput([FSLDIR + "/bin/fslval " + inputPaths[0] + " pixdim4"])
                print("TR is ", tr.replace("\n","").strip())
            if not totalVolumes == -1:
                print("Number of volumes specified by user. Will not get TR from input image")
            else:
                totalVolumes = subprocess.getoutput([FSLDIR + "/bin/fslnvols " + inputPaths[0]])
                print("Total volumes are", totalVolumes.replace("\n","").strip())


        elif self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            pass



