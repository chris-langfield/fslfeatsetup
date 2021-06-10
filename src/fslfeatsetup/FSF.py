import os
import re
import subprocess
from .FSFLabels import *
from .EVs import *
from .Comments import *
import fsl

class PyFSFError(Exception):
    """
    Generic error class for errors related to this module
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return 'Generic error'

# get $HOME

HOME = os.getenv("HOME")
print(HOME)

# get $FSLDIR
FSLDIR = os.getenv("FSLDIR")
if FSLDIR:
    print("$FSLDIR:",FSLDIR)
else:
    raise PyFSFError("[!] Could not find environment variable $FSLDIR. Is FSL installed?")


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

## get standard images
class FeatStandardImg:
    FMRIB58_FA_skeleton_1mm = FSLDIR + "/data/standard/FMRIB58_FA-skeleton_1mm"
    FSL_HCP1065_V1_1mm = FSLDIR + "/data/standard/FSL_HCP1065_V1_1mm"
    MNI152_T1_1mm_BigFoV_facemask = FSLDIR + "/data/standard/MNI152_T1_1mm_BigFoV_facemask"
    MNI152_T1_2mm_LR_masked = FSLDIR + "/data/standard/MNI152_T1_2mm_LR-masked"
    MNI152_T1_2mm_edges = FSLDIR + "/data/standard/MNI152_T1_2mm_edges"
    FMRIB58_FA_1mm = FSLDIR + "/data/standard/FMRIB58_FA_1mm"
    FSL_HCP1065_V2_1mm = FSLDIR + "/data/standard/FSL_HCP1065_V2_1mm"
    MNI152_T1_1mm_Hipp_mask_dil8 = FSLDIR + "MNI152_T1_1mm_Hipp_mask_dil8/data/standard/"
    MNI152_T1_2mm_VentricleMask = FSLDIR + "/data/standard/MNI152_T1_2mm_VentricleMask"
    MNI152_T1_2mm_eye_mask = FSLDIR + "/data/standard/MNI152_T1_2mm_eye_mask"
    FSL_HCP1065_FA_1mm = FSLDIR + "/data/standard/FSL_HCP1065_FA_1mm"
    FSL_HCP1065_V3_1mm = FSLDIR + "/data/standard/FSL_HCP1065_V3_1mm"
    MNI152_T1_1mm_brain = FSLDIR + "/data/standard/MNI152_T1_1mm_brain"
    MNI152_T1_2mm_b0 = FSLDIR + "/data/standard/MNI152_T1_2mm_b0"
    MNI152_T1_2mm_skull = FSLDIR + "/data/standard/MNI152_T1_2mm_skull"
    FSL_HCP1065_L1_1mm = FSLDIR + "/data/standard/FSL_HCP1065_L1_1mm"
    FSL_HCP1065_tensor_1mm = FSLDIR + "/data/standard/FSL_HCP1065_tensor_1mm"
    MNI152_T1_1mm_brain_mask = FSLDIR + "/data/standard/MNI152_T1_1mm_brain_mask"
    MNI152_T1_2mm_brain = FSLDIR + "/data/standard/MNI152_T1_2mm_brain"
    MNI152_T1_2mm_strucseg = FSLDIR + "/data/standard/MNI152_T1_2mm_strucseg"
    FSL_HCP1065_L2_1mm = FSLDIR + "/data/standard/FSL_HCP1065_L2_1mm"
    Fornix_FMRIB_FA1mm = FSLDIR + "/data/standard/Fornix_FMRIB_FA1mm"
    MNI152_T1_1mm_brain_mask_dil = FSLDIR + "/data/standard/MNI152_T1_1mm_brain_mask_dil"
    MNI152_T1_2mm_brain_mask = FSLDIR + "/data/standard/MNI152_T1_2mm_brain_mask"
    MNI152_T1_2mm_strucseg_periph = FSLDIR + "/data/standard/MNI152_T1_2mm_strucseg_periph"
    FSL_HCP1065_L3_1mm = FSLDIR + "/data/standard/FSL_HCP1065_L3_1mm"
    LowerCingulum_1mm = FSLDIR + "/data/standard/LowerCingulum_1mm"
    MNI152_T1_1mm_first_brain_mask = FSLDIR + "/data/standard/MNI152_T1_1mm_first_brain_mask"
    MNI152_T1_2mm_brain_mask_deweight_eyes = FSLDIR + "/data/standard/MNI152_T1_2mm_brain_mask_deweight_eyes"
    FSL_HCP1065_MD_1mm = FSLDIR + "/data/standard/FSL_HCP1065_MD_1mm"
    MNI152_T1_05mm = FSLDIR + "/data/standard/MNI152_T1_0.5mm"
    MNI152_T1_1mm_subbr_mask = FSLDIR + "/data/standard/MNI152_T1_1mm_subbr_mask"
    MNI152_T1_2mm_brain_mask_dil = FSLDIR + "/data/standard/MNI152_T1_2mm_brain_mask_dil"
    FSL_HCP1065_MO_1mm = FSLDIR + "/data/standard/FSL_HCP1065_MO_1mm"
    MNI152_T1_1mm = FSLDIR + "/data/standard/MNI152_T1_1mm"
    MNI152_T1_2mm = FSLDIR + "/data/standard/MNI152_T1_2mm"
    MNI152_T1_2mm_brain_mask_dil1 = FSLDIR + "/data/standard/MNI152_T1_2mm_brain_mask_dil1"


class FeatSettings:
    def __init__(self, LEVEL, # int
                 ANALYSIS,  # int
                 defaultsFilename=DEFAULT_SETTINGS_PATH): # filepath


        self.settings = {}
        self.defaults = {}
        self.inputs = []
        self.altRefImages = []
        self.b0fieldMaps = []
        self.b0Magnitudes = []
        self.mainStructuralImages = []
        self.expandedFunctionalImages = []

        # list of FirstLevelEV or HigherLevelEV objects (EVs.py)
        self.EVs = []
        # list of Contrast objects (EVs.py)
        self.Contrasts = []
        # list of 1s and 0s
        self.GroupMembership = []
        # list of lists of 1s and 0s
        self.Ortho = []

        if LEVEL not in [FeatLevel.HIGHER_LEVEL, FeatLevel.FIRST_LEVEL]:
            raise PyFSFError("Level must be FeatLevel.HIGHER_LEVEL or FeatLevel.FIRST_LEVEL")
        self.LEVEL = LEVEL
        if ANALYSIS not in [FeatAnalysis.STATS, FeatAnalysis.PREPROCESSING, FeatAnalysis.FULL_ANALYSIS]:
            raise PyFSFError("Analysis must be FeatAnalysis.STATS, FeatAnalysis.PREPROCESSING, or FeatAnalysis.FULL_ANALYSIS")
        self.ANALYSIS = ANALYSIS
        self.settings["level"] = LEVEL
        self.settings["analysis"] = ANALYSIS

        # FEAT version
        self.settings["version"] = FEAT_VERSION

        # Some defaults not appearing in GUI

        self.settings["relative_yn"] = 0

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

    def setOption(self, option, value):
        if option in self.settings:
            print(f"old setting: {option} = {self.settings[option]}")
            self.settings[option] = value
            print(f"new setting: {option} = {self.settings[option]}")
        else:
            print(option, "not currently in settings. May cause an error if not recognized by FEAT")
            self.settings[option] = value

    def printSettings(self):
        for option in self.settings:
            print(option,'--',self.settings[option])

    def write(self, path):
        """
        Collects all the configurations set by the child classes and writes out to an .fsf file.
        :param path: filepath to the .fsf file
        :return: None
        """
        with open(path,"w") as outFile:
            for s in self.settings:
                if s in Comments:
                    outFile.write(Comments[s])
                else:
                    print(s, "not in Comments")
                outFile.write("set fmri(" + s + ") " + str(self.settings[s]) + "\n\n")
            for i in range(len(self.inputs)):
                outFile.write("set feat_files(" + str(i+1) + ") \"" + self.inputs[i] + "\"\n\n")
            for i in range(len(self.mainStructuralImages)):
                outFile.write("set highres_files(" + str(i+1) + ") \"" + self.mainStructuralImages[i] + "\"\n\n")
            if self.LEVEL == FeatLevel.FIRST_LEVEL:
                outFile.write("# Number of EVs\n")
                outFile.write(f"set fmri(evs_orig) {len(self.EVs)}\n")
                outFile.write(f"set fmri(evs_real) {len(self.EVs)}\n")
                outFile.write(f"set fmri(evs_vox) 0\n\n")

                # not implemented yet
                outFile.write(f"set fmri(motionevsbeta) \"\"\n")
                outFile.write(f"set fmri(scriptevsbeta) \"\"\n\n")

                # since this is first level
                outFile.write("# Number of lower-level copes feeding into higher-level analysis\n")
                outFile.write("set fmri(ncopeinputs) 0\n\n")

                for e in range(len(self.EVs)):
                    outFile.write(f"# EV {e+1} title\n")
                    outFile.write("set fmri(evtitle" + str(e+1) + ") \"" + self.EVs[e].name + "\"\n\n")
                    outFile.write(f"# Basic waveform shape (EV {e+1})\n# 0 : Square\n# 1 : Sinusoid\n# 2 : Custom (1 entry per volume)\n# 3 : Custom (3 column format)\n# 4 : Interaction\n# 10 : Empty (all zeros)\n")
                    outFile.write("set fmri(shape" + str(e+1) + ") " + str(self.EVs[e].shape) + "\n\n")
                    outFile.write(f"# Convolution (EV {e+1})\n# 0 : None\n# 1 : Gaussian\n# 2 : Gamma\n# 3 : Double-Gamma HRF\n# 4 : Gamma basis functions\n# 5 : Sine basis functions\n# 6 : FIR basis functions\n")
                    outFile.write("set fmri(convolve" + str(e+1) + ") " + str(self.EVs[e].hrf.idx) + "\n\n")
                    outFile.write(self.EVs[e].hrf.write(e+1))
                    outFile.write(f"# Apply temporal filtering (EV {e+1})\n")
                    outFile.write("set fmri(tempfilt_yn" + str(e+1) + ") " + str(int(self.EVs[e].temporalFiltering)) + "\n\n")
                    outFile.write(f"# Add temporal derivative (EV {e+1})\n")
                    outFile.write("set fmri(deriv_yn" + str(e+1) + ") " + str(int(self.EVs[e].temporalDerivative)) + "\n\n")
                    outFile.write(f"# Custom EV file (EV {e+1})\n")
                    outFile.write("set fmri(custom" + str(e+1) + ") \"" + self.EVs[e].filename + "\"\n\n")

                outFile.write("# Contrast & F-tests mode\n")
                outFile.write("# real : control real EVs\n")
                outFile.write("# orig : control original EVs\n")
                outFile.write("set fmri(con_mode_old) orig\n")
                outFile.write("set fmri(con_mode) orig\n")

                outFile.write("# Number of Contrasts\n")
                outFile.write(f"set fmri(ncon_orig) {len(self.Contrasts)}\n")
                outFile.write(f"set fmri(ncon_real) {len(self.Contrasts)}\n\n")

                for c in range(len(self.Contrasts)):
                    outFile.write("# Display images for contrast_real 1\n")
                    outFile.write(f"set fmri(conpic_real.{c+1}) 1\n\n")
                    outFile.write(f"# Title for contrast_real {c+1}\n")
                    outFile.write(f"set fmri(conname_real.{c+1}) \"{self.Contrasts[c].name}\"\n\n")
                    for i in range(len(self.Contrasts[c].vector)):
                        outFile.write(f"# Real contrast_real vector {c+1} element {i+1}\n")
                        outFile.write(f"set fmri(con_real{c+1}.{i+1}) {self.Contrasts[c].vector[i]}\n\n")

                for c in range(len(self.Contrasts)):
                    outFile.write("# Display images for contrast_orig 1\n")
                    outFile.write(f"set fmri(conpic_orig.{c+1}) 1\n\n")
                    outFile.write(f"# Title for contrast_orig {c+1}\n")
                    outFile.write(f"set fmri(conname_orig.{c+1}) \"{self.Contrasts[c].name}\"\n\n")
                    for i in range(len(self.Contrasts[c].vector)):
                        outFile.write(f"# Real contrast_orig vector {c+1} element {i+1}\n")
                        outFile.write(f"set fmri(con_orig{c+1}.{i+1}) {self.Contrasts[c].vector[i]}\n\n")


                outFile.write("# Number of F-tests\n")
                outFile.write(f"set fmri(nftests_orig) 0\n")
                outFile.write(f"set fmri(nftests_real) 0\n\n")

            if self.LEVEL == FeatLevel.HIGHER_LEVEL:
                for e in range(len(self.EVs)):
                    outFile.write("set fmri(evtitle" + str(e + 1) + ") \"" + self.EVs[e].name + "\"\n\n")
                    for i in range(len(self.EVs[e].vector)):
                        outFile.write(f"set fmri(evg{e+1}.{i+1}) {self.EVs[e].vector[i]}\n\n")

                for g in range(len(self.GroupMembership)):
                    outFile.write(f"set fmri(groupmem.{g+1}) {self.GroupMembership[g]}\n\n")

                for c in range(len(self.Contrasts)):
                    outFile.write(f"set fmri(conpic_real.{c+1}) 1\n\n")
                    outFile.write(f"set fmri(conname_real.{c+1}) \"{self.Contrasts[c].name}\"\n\n")
                    for x in range(len(self.Contrasts[c].vector)):
                        outFile.write(f"set fmri(con_real{c+1}.{x+1}) {self.Contrasts[c].vector[x]}\n\n")

            # length of orthogonalization vector is number of EVs plus 1 because you have to account for the null event 0
            for o in range(1, len(self.Ortho)):
                for p in range(len(self.Ortho[o])):
                    outFile.write(f"# Orthogonalise EV {o} wrt EV {p}\n")
                    outFile.write(f"set fmri(ortho{o}.{p}) {self.Ortho[o][p]}\n\n")


class DataOptions:
    """
    Must be a child object of a FeatSettings instance.
    This child must be created and configured before the others.
    """
    def __init__(self, myFeatSettings):
        self.parent = myFeatSettings
        # default
        if "paradigm_hp" in self.parent.defaults:
            self.DEFAULT_HIGHPASS_CUTOFF = int(self.parent.defaults["paradigm_hp"])
        if "ndelete" in self.parent.defaults:
            self.DEFAULT_DELETE_VOLUMES = self.parent.defaults["ndelete"]

    def Configure(self, outputDirectory, # filepath
                  inputPaths,  # list of filepaths
                  totalVolumes=-1,  # int
                  deleteVolumes = -1, # int
                  tr =-1, # int
                  highPassCutoff = -1, # int
                  higherLevelInput = FeatHigherLevelInput.COPE_IMAGES): # int
        """
        Takes parameters corresponding to the "Data" tab in the FEAT GUI. It then updates the settings list of its FeatSettings parent class.
        :param outputDirectory: Mandatory .feat or .gfeat path
        :param inputPaths: Mandatory list of input filepaths
        :param totalVolumes: Optional number of volumes per input. Can be inferred if left blank.
        :param deleteVolumes: Optional number of volumes to delete. Will be set to default found in defaults file, or otherwise set to 0
        :param tr: Optional TR of input images. Can be inferred if left blank.
        :param highPassCutoff: Optional, unless default file does not contain this setting
        :param higherLevelInput: Optional, for higher-level analyses only. Can be set to 1 (lower-level feat directories) or 2 (lower level cope images), or using the built-in type FeatHigherLevelInput.FEAT_DIRS or FeatHigherLevelInput.COPE_IMAGES
        :return: None
        """

        if inputPaths in [[], None]:
            raise PyFSFError("No inputs were provided!")

        if not os.path.exists(inputPaths[0]):
            raise PyFSFError(inputPaths[0] + " does not exist!")

        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:

            if not tr == -1:
                print("TR specified by user. Will not get TR from input image")
                try:
                    int(tr)
                except ValueError:
                    raise PyFSFError("TR must be int")
                self.parent.settings["tr"] = tr
            else:
                tr = subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " pixdim4")
                if "Exception" in tr:
                    raise PyFSFError("Could not get TR from input image. fslval output: " + tr)
                self.parent.settings["tr"] = float(tr.replace("\n","").strip())
                print("TR is ", tr.replace("\n","").strip())
            if not totalVolumes == -1:
                print("Number of volumes specified by user. Will not get TR from input image")
                try:
                    int(totalVolumes)
                except ValueError:
                    raise PyFSFError("Total volumes must be int")
                self.parent.settings["npts"] = totalVolumes
            else:
                totalVolumes = subprocess.getoutput(FSLDIR + "/bin/fslnvols " + inputPaths[0])
                if "Exception" in totalVolumes:
                    raise PyFSFError("Could not get number of volumes from input images. fslnvols output: " + totalVolumes)
                self.parent.settings["npts"] = int(totalVolumes.replace("\n","").strip())
                print("Total volumes are", totalVolumes.replace("\n","").strip())

            if deleteVolumes == -1:
                if hasattr(self, 'DEFAULT_DELETE_VOLUMES'):
                    deleteVolumes = self.DEFAULT_DELETE_VOLUMES
                else:
                    deleteVolumes = 0
            else:
                try:
                    int(deleteVolumes)
                except ValueError:
                    raise PyFSFError("Number of deleted volumes must be int")
            self.parent.settings["ndelete"] = deleteVolumes

            if highPassCutoff == -1:
                if hasattr(self, 'DEFAULT_HIGHPASS_CUTOFF'):
                    highPassCutoff = self.DEFAULT_HIGHPASS_CUTOFF
                else:
                    highPassCutoff = 100
            else:
                try:
                    int(highPassCutoff)
                except ValueError:
                    raise PyFSFError("highPassCutoff must be int")
            self.parent.settings["paradigm_hp"] = highPassCutoff

        elif self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            self.parent.settings["inputtype"] = higherLevelInput
            self.parent.settings["npts"] = len(inputPaths)

        self.parent.settings["outputdir"] = "\"" + outputDirectory + "\""
        self.parent.settings["multiple"] = len(inputPaths)

        # input paths

        for i in range(len(inputPaths)):
            self.parent.inputs.append(inputPaths[i])


        ## voxel size
        try:
            dim1 = int(
                subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
            dim2 = int(
                subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
            dim3 = int(
                subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
            dim4 = int(
                subprocess.getoutput(FSLDIR + "/bin/fslval " + inputPaths[0] + " dim1").replace("\n", "").strip())
        except:
            raise PyFSFError("Problem with getting image dimensions for " + inputPaths[0])

        totalVoxels = dim1 * dim2 * dim3 * dim4
        self.parent.settings["totalVoxels"] = totalVoxels



    def printSettings(self):
        print("Data Settings: " + self.parent.settings["outputdir"])
        print(FeatLevelToStr[self.parent.LEVEL], "|", FeatAnalysisToStr[self.parent.ANALYSIS])
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
    """
    Must be a child object of a FeatSettings instance.
    """
    def __init__(self, parent):
        self.parent = parent
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

    def Configure(self,
                  brainThreshold=-1, # int
                  noiseLevel=-1, # float
                  temporalSmoothness=-1, # float
                  zThreshold=-1, # float
                  cleanupFirstLevel=None, # bool
                  overwriteOriginalPostStats = None, # bool
                  estimateNoiseFromData=False):
        """
        Takes parameters corresponding to the "Misc" tab in the FEAT GUI. It then updates the settings list of its FeatSettings parent class.

        :param brainThreshold: Optional unless not specified in defaults file
        :param noiseLevel: Optional unless not specified in defaults file
        :param temporalSmoothness: Optional unless not specified in defaults file
        :param zThreshold: Optional unless not specified in defaults file
        :param cleanupFirstLevel: Optional unless not specified in defaults file
        :param overwriteOriginalPostStats: Optional unless not specified in defaults file
        :param estimateNoiseFromData: TODO
        :return: None
        """

        if brainThreshold == -1:
            if hasattr(self, 'DEFAULT_BRAIN_THRESH'):
                brainThreshold = self.DEFAULT_BRAIN_THRESH
            else:
                brainThreshold = 10
        else:
            try:
                int(brainThreshold)
            except ValueError:
                raise PyFSFError("Brain threshold must be int")
        self.parent.settings["brain_thresh"] = brainThreshold

        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:

            if noiseLevel == -1:
                if hasattr(self, 'DEFAULT_NOISE'):
                    noiseLevel = self.DEFAULT_NOISE
                else:
                    noiseLevel = 0.66
            else:
                try:
                    float(noiseLevel)
                except ValueError:
                    raise PyFSFError("Noise level must be float")
            self.parent.settings["noise"] = noiseLevel

            if temporalSmoothness == -1:
                if hasattr(self, 'DEFAULT_SMOOTHNESS'):
                    temporalSmoothness = self.DEFAULT_SMOOTHNESS
                else:
                    temporalSmoothness = 0.34
            else:
                try:
                    float(temporalSmoothness)
                except ValueError:
                    raise PyFSFError("Temporal smoothness must be float")
            self.parent.settings["noisear"] = temporalSmoothness

            if zThreshold == -1:
                if hasattr(self, 'DEFAULT_CRITICAL_Z'):
                    zThreshold = self.DEFAULT_CRITICAL_Z
                else:
                    zThreshold = 5.3
            else:
                try:
                    float(zThreshold)
                except ValueError:
                    raise PyFSFError("Z threshold must be float")
            self.parent.settings["critical_z"] = zThreshold

        if self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            if cleanupFirstLevel is None:
                if hasattr(self, 'DEFAULT_CLEANUP_FIRSTLEVEL_YN'):
                    cleanupFirstLevel = self.DEFAULT_CLEANUP_FIRSTLEVEL_YN
                else:
                    cleanupFirstLevel = False
            else:
                if cleanupFirstLevel not in [True, False]:
                    raise PyFSFError("Cleanup First Level must be bool")
            self.parent.settings["sscleanup"] = int(cleanupFirstLevel)

            if overwriteOriginalPostStats is None:
                if hasattr(self, 'DEFAULT_OVERWRITE_POSTSTATS'):
                    overwriteOriginalPostStats = self.DEFAULT_OVERWRITE_POSTSTATS
                else:
                    overwriteOriginalPostStats = False
            else:
                if overwriteOriginalPostStats not in [True, False]:
                    raise PyFSFError("overwriteOriginalPostStats must be bool")
            self.parent.settings["newdir_yn"] = int(overwriteOriginalPostStats)



    def printSettings(self):
        print("Misc Settings: " + self.parent.settings["outputdir"])
        print(FeatLevelToStr[self.parent.LEVEL], "|", FeatAnalysisToStr[self.parent.ANALYSIS])
        print("--------------")
        print("Brain/background threshold:", self.parent.settings["brain_thresh"])
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:
            print("Noise level %:", self.parent.settings["noise"])
            print("Temporal smoothness:", self.parent.settings["noisear"])
            print("Z-threshold:", self.parent.settings["critical_z"])
        if self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            print("Cleanup first level standard-space images", self.parent.settings["sscleanup"])



class PreStatsOptions:
    def __init__(self, parent):
        self.parent = parent
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
                  perfusionTagControlOrder = None, # int
                  highPassTemporalFilter = None, # bool
                  lowPassTemporalFilter = None, # bool
                  usingAlternateReferenceImage = None, # bool
                  alternateReferenceImages = None): ## list of paths

        """
        Takes parameters corresponding to the "Pre-stats" tab in the FEAT GUI. It then updates the settings list of its FeatSettings parent class.
        :param mcflirt: Optional unless not specified in defaults file
        :param b0_unwarp: Optional unless not specified in defaults file
        :param melodic: Optional unless not specified in defaults file
        :param sliceTiming: Optional, defaults to 0
        :param sliceTimingFile: Mandatory depending on `sliceTiming`
        :param bet: Optional unless not specified in defaults file
        :param spatialSmoothing: Optional unless not specified in defaults file
        :param intensityNormalization: Optional unless not specified in defaults file
        :param perfusionSubtraction: Optional unless not specified in defaults file
        :param perfusionTagControlOrder: Optional unless not specified in defaults file
        :param highPassTemporalFilter: Optional unless not specified in defaults file
        :param lowPassTemporalFilter: Optional unless not specified in defaults file
        :param usingAlternateReferenceImage: Optional unless not specified in defaults file
        :param alternateReferenceImages: Mandatory list of images, one per input, if `usingAlternateReferenceImage` is true
        :return:
        None
        """

        if mcflirt is None:
            if hasattr(self, 'DEFAULT_MCFLIRT'):
                mcflirt = self.DEFAULT_MCFLIRT
            else:
                mcflirt = 0
        else:
            if mcflirt not in [True, False]:
                raise PyFSFError("MCFLIRT option must be bool")
        self.parent.settings["mc"] = int(mcflirt)

        if b0_unwarp is None:
            if hasattr(self, 'DEFAULT_B0_UNWARP'):
                b0_unwarp = self.DEFAULT_B0_UNWARP
            else:
                b0_unwarp = False
        else:
            if b0_unwarp not in [True, False]:
                raise PyFSFError("b0_unwarp option must be bool")
        self.parent.settings["regunwarp_yn"] = int(b0_unwarp)

        if melodic is None:
            if hasattr(self, 'DEFAULT_MELODIC'):
                melodic = self.DEFAULT_MELODIC
            else:
                melodic = False
        else:
            if melodic not in [True, False]:
                raise PyFSFError("melodic option must be bool")
        self.parent.settings["melodic_yn"] = int(melodic)

        if sliceTiming is None:
            if hasattr(self, 'DEFAULT_SLICE_TIMING'):
                sliceTiming = self.DEFAULT_SLICE_TIMING
            else:
                sliceTiming = FeatSliceTiming.NONE
        else:
            if sliceTiming not in FeatSliceTiming.Options:
                raise PyFSFError("Slice timing option must be in FeatSliceTiming.Options")
        self.parent.settings["st"] = sliceTiming

        if bet is None:
            if hasattr(self, 'DEFAULT_BET'):
                bet = self.DEFAULT_BET
            else:
                bet = False
        else:
            if bet not in [True, False]:
                raise PyFSFError("BET option must be bool")
        self.parent.settings["bet_yn"] = int(bet)

        if spatialSmoothing is None:
            if hasattr(self, 'DEFAULT_SMOOTH'):
                spatialSmoothing = self.DEFAULT_SMOOTH
            else:
                spatialSmoothing = 5.0
        else:
            try:
                float(spatialSmoothing)
            except ValueError:
                raise PyFSFError("Spatial smoothing must be float")
        self.parent.settings["smooth"] = spatialSmoothing

        if sliceTimingFile is None:
            if self.parent.settings["st"] not in [FeatSliceTiming.NONE, FeatSliceTiming.INTERLEAVED, FeatSliceTiming.REGULAR_DOWN, FeatSliceTiming.REGULAR_UP]:
                raise PyFSFError("Slice timing or slice order file is required")
        else:
            self.parent.settings["st_file"] = "\"" + sliceTimingFile + "\""

        if intensityNormalization is None:
            if hasattr(self, 'DEFAULT_NORM'):
                intensityNormalization = self.DEFAULT_NORM
            else:
                intensityNormalization = False
        else:
            if intensityNormalization not in [True, False]:
                raise PyFSFError("intensity normalization option must be bool")
        self.parent.settings["norm_yn"] = int(intensityNormalization)

        if perfusionSubtraction is None:
            if hasattr(self, 'DEFAULT_PERFSUB'):
                perfusionSubtraction = self.DEFAULT_PERFSUB
            else:
                perfusionSubtraction = False
        else:
            if perfusionSubtraction not in [True, False]:
                raise PyFSFError("Perfusion subtraction option must be bool")
        self.parent.settings["perfsub_yn"] = int(perfusionSubtraction)

        if perfusionTagControlOrder is None:
            if hasattr(self, 'DEFAULT_PERF_TAGFIRST'):
                perfusionTagControlOrder = self.DEFAULT_PERF_TAGFIRST
            else:
                perfusionTagControlOrder = FeatPerfusion.FirstTimepointIsTag
        else:
            if perfusionTagControlOrder not in FeatPerfusion.Options:
                raise PyFSFError("Perfusion tag control order must be in FeatPerfusion.Options. Or use 0 or 1.")
        self.parent.settings["tagfirst"] = perfusionTagControlOrder

        if highPassTemporalFilter is None:
            if hasattr(self, 'DEFAULT_TEMPORAL_HIGHPASS'):
                highPassTemporalFilter = self.DEFAULT_TEMPORAL_HIGHPASS
            else:
                highPassTemporalFilter = False
        else:
            if highPassTemporalFilter not in [True, False]:
                raise PyFSFError("High pass temporal filter option must be bool")
        self.parent.settings["temphp_yn"] = int(highPassTemporalFilter)

        if lowPassTemporalFilter is None:
            if hasattr(self, 'DEFAULT_TEMPORAL_LOWPASS'):
                lowPassTemporalFilter = self.DEFAULT_TEMPORAL_LOWPASS
            else:
                lowPassTemporalFilter = False
        else:
            if lowPassTemporalFilter not in [True, False]:
                raise PyFSFError("Low pass temporal filter option must be bool")
        self.parent.settings["templp_yn"] = int(lowPassTemporalFilter)

        if usingAlternateReferenceImage is None:
            if hasattr(self, 'DEFAULT_ALT_REF_IMG'):
                usingAlternateReferenceImage = self.DEFAULT_ALT_REF_IMG
            else:
                usingAlternateReferenceImage = False
        else:
            if usingAlternateReferenceImage not in [True, False]:
                raise PyFSFError("Use Alternate Reference Image option must be bool")
        self.parent.settings["alternativeReference_yn"] = int(usingAlternateReferenceImage)

        if alternateReferenceImages is None:
            if usingAlternateReferenceImage:
                raise PyFSFError("Must specify at least one alternate reference image if usingAlternateReferenceImage is set to True")
        else:
            if not len(alternateReferenceImages) == len(self.parent.inputs):
                raise PyFSFError("Number of alternate reference images does not match number of inputs")
            for i in range(0, len(self.parent.inputs)):
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
        """
        Optionally sets up the B0 Unwarping fields. Must have already run `Configure()`
        :param fieldmapImages: Mandatory list of images, one for each input
        :param fieldmapMagnitudeImages: Mandatory list of images, one for each input
        :param epiDwell: Optional unless not specified in defaults file
        :param epiTE: Optional unless not specified in defaults file
        :param unwarpDir: Optional unless not specified in defaults file
        :param signalLoss: Optional unless not specified in defaults file
        :return: None
        """
        if not self.CONFIGURED:
            raise PyFSFError("The Pre-Stats options have not been configured. Use PreStatsOptions.Configure()")
        if fieldmapImages in [[], None]:
            raise PyFSFError("Error: specify fieldmap images")
        elif not len(fieldmapImages) == len(self.parent.inputs):
            raise PyFSFError("Number of fieldmap images does not match number of inputs")
        if fieldmapMagnitudeImages in [[], None]:
            raise PyFSFError("Error: specify fieldmap magnitude images")
        elif not len(fieldmapMagnitudeImages) == len(self.parent.inputs):
            raise PyFSFError("Number of fieldmap magnitude images does not match number of inputs")

        for i in range(0, len(self.parent.inputs)):
            self.parent.b0fieldMaps.append(fieldmapImages[i])
        for i in range(0, len(self.parent.inputs)):
            self.parent.b0Magnitudes.append(fieldmapMagnitudeImages[i])

        if epiDwell is None:
            if hasattr(self, 'DEFAULT_EPI_DWELL'):
                epiDwell = self.DEFAULT_EPI_DWELL
            else:
                epiDwell = 0.0
        else:
            try:
                float(epiDwell)
            except ValueError:
                raise PyFSFError("epiDwell must be float")
        self.parent.settings["dwell"] = epiDwell

        if epiTE is None:
            if hasattr(self, 'DEFAULT_EPI_TE'):
                epiTE = self.DEFAULT_EPI_TE
            else:
                epiTE = 0.0
        else:
            if epiTE not in [True, False]:
                raise PyFSFError("epiTE option must be float")
        self.parent.settings["te"] = epiTE

        if signalLoss is None:
            if hasattr(self,'DEFAULT_SIGNAL_LOSS'):
                signalLoss = self.DEFAULT_SIGNAL_LOSS
            else:
                signalLoss = 10
        else:
            if signalLoss not in [True, False]:
                raise PyFSFError("Signal loss option must be int")
        self.parent.settings["signallossthresh"] = signalLoss

        if unwarpDir is None:
            if hasattr(self, 'DEFAULT_UNWARP_DIR'):
                unwarpDir = self.DEFAULT_UNWARP_DIR
            else:
                unwarpDir = FeatUnwarp.Y_MINUS
        else:
            if unwarpDir not in FeatUnwarp.Directions:
                raise PyFSFError("unwarpDir must be in FeatUnwarp.Directions")
        self.parent.settings["unwarp_dir"] = unwarpDir

class RegOptions:
    def __init__(self, parent):
        self.parent = parent
        if "reghighres_search" in self.parent.defaults:
            self.DEFAULT_MAIN_STRUCTURAL_SEARCH = int(self.parent.defaults["reghighres_search"])
        if "reghighres_dof" in self.parent.defaults:
            self.DEFAULT_MAIN_STRUCTURAL_DOF = self.parent.defaults["reghighres_dof"]
        if "initial_highres_search" in self.parent.defaults:
            self.DEFAULT_EXPANDED_FUNCTIONAL_SEARCH = int(self.parent.defaults["initial_highres_search"])
        if "initial_highres_dof" in self.parent.defaults:
            self.DEFAULT_EXPANDED_FUNCTIONAL_DOF = int(self.parent.defaults["initial_highres_dof"])
        if "regstandard" in self.parent.defaults:
            self.DEFAULT_STANDARD = self.parent.defaults["regstandard"]
        if "regstandard_search" in self.parent.defaults:
            self.DEFAULT_STANDARD_SEARCH = int(self.parent.defaults["regstandard_search"])
        if "regstandard_dof" in self.parent.defaults:
            self.DEFAULT_STANDARD_DOF = int(self.parent.defaults["regstandard_dof"])
        if "regstandard_nonlinear_yn" in self.parent.defaults:
            if int(self.parent.defaults["regstandard_nonlinear_yn"]) == 1:
                self.DEFAULT_STANDARD_NONLINEAR = True
            else:
                self.DEFAULT_STANDARD_NONLINEAR = False
        if "regstandard_nonlinear_warpres" in self.parent.defaults:
            self.DEFAULT_STANDARD_WARPRES = int(self.parent.defaults["regstandard_nonlinear_warpres"])

        ## hack to prevent an error TODO
        if "fnirt_config" in self.parent.defaults:
            self.parent.settings["fnirt_config"] = "\"" + FSLDIR + "/data/standard/" + self.parent.defaults[
                "fnirt_config"].replace("\"", "") + "\""

    def ConfigureMainStructural(self, mainStructuralImages, # list of filepaths
                   mainStructuralSearch = None, # int
                   mainStructuralDOF = None # string
                  ):

        # set reghighres_yn
        self.parent.settings["reghighres_yn"] = 1

        if mainStructuralImages in [[],None]:
            raise PyFSFError("No structural images were provided!")
        elif not len(mainStructuralImages) == len(self.parent.inputs):
            raise PyFSFError("Number of main structural images does not match number of inputs")

        for i in range(len(self.parent.inputs)):
            self.parent.mainStructuralImages.append(mainStructuralImages[i])

        if mainStructuralSearch is None:
            if hasattr(self, 'DEFAULT_MAIN_STRUCTURAL_SEARCH'):
                mainStructuralSearch = self.DEFAULT_MAIN_STRUCTURAL_SEARCH
            else:
                raise PyFSFError("No search strategy was selected for main structural image registration, and none was found in defaults")
        else:
            if mainStructuralSearch not in RegistrationSearch.Options:
                raise PyFSFError("mainStructuralSearch must be in RegistrationSearch.Options")
        self.parent.settings["reghighres_search"] = mainStructuralSearch

        if mainStructuralDOF is None:
            if hasattr(self, 'DEFAULT_MAIN_STRUCTURAL_DOF'):
                mainStructuralDOF = self.DEFAULT_MAIN_STRUCTURAL_DOF
            else:
                raise PyFSFError("No DOF for main structural registration was provided and none was found in defaults.")
        else:
            if not mainStructuralDOF == "BBR":
                raise PyFSFError("Only 'BBR' option is currently allowed for DOF for main structural registration")
        self.parent.settings["reghighres_dof"] = mainStructuralDOF

    def ConfigureExpandedFunctional(self, expandedFunctionalImages,
                                    expandedFunctionalSearch = None,
                                    expandedFunctionalDOF = None):

        # set reginitial_highres_yn
        self.parent.settings["reginitial_highres_yn"] = 1

        if expandedFunctionalImages in [[],None]:
            raise PyFSFError("No structural images were provided!")
        elif not len(expandedFunctionalImages) == len(self.parent.inputs):
            raise PyFSFError("Number of expanded functional images does not match number of inputs")

        for i in range(len(self.parent.inputs)):
            self.parent.expandedFunctionalImages.append(expandedFunctionalImages[i])

        if expandedFunctionalSearch is None:
            if hasattr(self, 'DEFAULT_EXPANDED_FUNCTIONAL_SEARCH'):
                expandedFunctionalSearch = self.DEFAULT_EXPANDED_FUNCTIONAL_SEARCH
            else:
                raise PyFSFError("No search strategy was selected for expanded functional image registration, and none was found in defaults")
        else:
            if expandedFunctionalSearch not in RegistrationSearch.Options:
                raise PyFSFError("mainStructuralRegSearch must be in RegistrationSearch.Options")
        self.parent.settings["initial_highres_search"] = expandedFunctionalSearch

        if expandedFunctionalDOF is None:
            if hasattr(self, 'DEFAULT_EXPANDED_FUNCTIONAL_DOF'):
                expandedFunctionalDOF = self.DEFAULT_EXPANDED_FUNCTIONAL_DOF
            else:
                raise PyFSFError("No DOF for main structural registration was provided and none was found in defaults.")
        else:
            if expandedFunctionalDOF not in RegistrationDOF.Options:
                raise PyFSFError("Expanded functional DOF must be 3,6,7,9 or 12")
        self.parent.settings["initial_highres_dof"] = expandedFunctionalDOF

    def ConfigureStandardSpace(self, standardImage = None, # filepath
                               standardSearch = None, # int
                               standardDOF = None, # int
                               doNonlinear = None, # bool
                               warpResolution = None # int
                               ):
        # set regstandard_yn
        self.parent.settings["regstandard_yn"] = 1

        if standardImage is None:
            if hasattr(self,'DEFAULT_STANDARD'):
                standardImage = self.DEFAULT_STANDARD
            else:
                raise PyFSFError("No standard image was specified and none was found in defaults")
        self.parent.settings["regstandard"] = standardImage.replace("${FSLDIR}", FSLDIR)

        if standardSearch is None:
            if hasattr(self, 'DEFAULT_STANDARD_SEARCH'):
                standardSearch = self.DEFAULT_STANDARD_SEARCH
            else:
                raise PyFSFError("No standard search was specified and none was found in defaults")
        else:
            if standardSearch not in RegistrationSearch.Options:
                raise PyFSFError("standardSearch must be in RegistrationSearch.Options: 0, 90 or 180")
        self.parent.settings["regstandard_search"] = standardSearch

        if standardDOF is None:
            if hasattr(self, 'DEFAULT_STANDARD_DOF'):
                standardDOF = self.DEFAULT_STANDARD_DOF
            else:
                raise PyFSFError("No standard DOF was specified and none was found in defaults")
        else:
            if standardDOF not in RegistrationDOF.Options:
                raise PyFSFError("Standard DOF must be in RegistrationDOF.Options")
        self.parent.settings["regstandard_dof"] = standardDOF

        if doNonlinear is None:
            if hasattr(self, 'DEFAULT_STANDARD_NONLINEAR'):
                doNonlinear = self.DEFAULT_STANDARD_NONLINEAR
            else:
                doNonlinear = False
        else:
            if doNonlinear not in [True,False]:
                raise PyFSFError("doNonLinear must be bool")
        self.parent.settings["regstandard_nonlinear_yn"] = int(doNonlinear)

        if doNonlinear:
            if warpResolution is None:
                if hasattr(self, 'DEFAULT_WARPRES'):
                    warpResolution = self.DEFAULT_WARPRES
                else:
                    raise PyFSFError("No Warp Resolution was specified and none was found in defaults, but Nonlinear registration is on!")
            else:
                try:
                    int(warpResolution)
                except ValueError:
                    raise PyFSFError("Warp resolution must be int")
            self.parent.settings["regstandard_nonlinear_warpres"] = warpResolution


class StatsOptions:
    def __init__(self,parent):
        self.parent = parent
        if "prewhiten_yn" in self.parent.defaults:
            if int(self.parent.defaults["prewhiten_yn"]) == 1:
                self.DEFAULT_PREWHITEN = True
            else:
                self.DEFAULT_PREWHITEN = False
        if "motionevs" in self.parent.defaults:
            self.DEFAULT_MOTION_EVS = int(self.parent.defaults["motionevs"])
        if "mixed_yn" in self.parent.defaults:
            self.DEFAULT_HIGHER_LEVEL_MODEL = int(self.parent.defaults["mixed_yn"])
        if "randomisePermutations" in self.parent.defaults:
            self.DEFAULT_RANDOMISE = int(self.parent.defaults["randomisePermutations"])
        if "robust_yn" in self.parent.defaults:
            if int(self.parent.defaults["robust_yn"]) == 1:
                self.DEFAULT_OUTLIER_DEWEIGHTING = True
            else:
                self.DEFAULT_OUTLIER_DEWEIGHTING = False

        ## this is pending functions to set up custom basis fxns from FLOBS
        if "default_bfcustom" in self.parent.defaults:
            self.parent.settings["default_bfcustom"] = self.parent.defaults["default_bfcustom"].replace("${FSLDIR}", FSLDIR)

        ## pending conmasking setup

        self.parent.settings["conmask1_1"] = 0


        # Do stats
        self.parent.settings["stats_yn"] = 1

    def Configure(self, preWhitening=None, addMotionEVs=None):
        """
        Configure the Stats settings.
        :param preWhitening: (bool) optional unless not specified in defaults
        :param addMotionEVs: (int) optional unless not specified in defaults. Must be in FeatMotionEV.Options
        :return: None
        """
        if preWhitening is None:
            if hasattr(self, 'DEFAULT_PREWHITEN'):
                preWhitening = int(self.DEFAULT_PREWHITEN)
            else:
                raise PyFSFError("No prewhitening was specified and none was found in defaults")
        else:
            if preWhitening not in [True, False]:
                raise PyFSFError("Prewhiting must be bool")
        self.parent.settings["prewhiten_yn"] = int(preWhitening)

        if addMotionEVs is None:
            if hasattr(self, 'DEFAULT_MOTION_EVS'):
                addMotionEVs = int(self.DEFAULT_MOTION_EVS)
            else:
                raise PyFSFError("No motion EVs choice was specified and none was found in defaults")
        else:
            if addMotionEVs not in FeatMotionEV.Options:
                raise PyFSFError("addMotionEVs must be in FeatMotionEV.Options")
        self.parent.settings["motionevs"] = addMotionEVs

    def AddFirstLevelEV(self, name, filename, hrf, temporalDerivative=False, temporalFiltering=True):
        if self.parent.LEVEL == FeatLevel.HIGHER_LEVEL:
            raise PyFSFError("Cannot add a first level EV to a higher-level analysis!")
        newEV = FirstLevelEV(name, filename, hrf, temporalDerivative, temporalFiltering)
        self.parent.EVs.append(newEV)

    def AddHigherLevelEV(self, name, vector):
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:
            raise PyFSFError("Cannot add a higher level EV to a first level analysis!")
        newEV = HigherLevelEV(name, vector)
        self.parent.EVs.append(newEV)

    def AddContrast(self, name, vector):
        newContrast = Contrast(name, vector)
        self.parent.Contrasts.append(newContrast)

    def Groups(self, vector):
        if self.parent.LEVEL == FeatLevel.FIRST_LEVEL:
            raise PyFSFError("Cannot assign group membership to inputs in first-level analysis")
        self.parent.GroupMembership = vector

    def OrthogonalizeEVs(self, matrix):
        ## matrix is a list of lists with length and with numberOfEVs + 1 because you have to include the null (0) EV
        self.parent.Ortho = matrix

    def ConfigureHigherLevel(self, model=None, outlierDeweighting = None, randomisePermutations=None):
        """
        Configure higher level options
        :param model: (int) must be FSFLabels.HigherLevelModeling.Options
        :param outlierDeweighting: (bool) optional unless not specified in defaults
        :param randomisePermutations: (int) optional unless not specified in defaults
        :return:
        """
        if model not in HigherLevelModeling.Options:
            raise PyFSFError("Higher level model must be in HigherLevelModeling.Options")

        if model is None:
            if hasattr(self, 'DEFAULT_HIGHER_LEVEL_MODEL'):
                model = self.DEFAULT_HIGHER_LEVEL_MODEL
            else:
                raise PyFSFError("No higher level model was assigned and none was found in defaults")
        self.parent.settings["mixed_yn"] = model

        if outlierDeweighting is None:
            if hasattr(self, 'DEFAULT_OUTLIER_DEWEIGHTING'):
                outlierDeweighting = self.DEFAULT_OUTLIER_DEWEIGHTING
            else:
                raise PyFSFError("No outlier deweighting option was chosen and none was found in defaults")
        self.parent.settings["robust_yn"] = int(outlierDeweighting)
        if randomisePermutations is None:
            if hasattr(self, 'DEFAULT_RANDOMISE'):
                randomisePermutations = self.DEFAULT_RANDOMISE
            else:
                raise PyFSFError("Randomise permutations was not set and was not found in defaults")
        else:
            try:
                int(randomisePermutations)
            except ValueError:
                raise PyFSFError("Randomise permutations must be int")
        self.parent.settings["randomisePermutations"] = randomisePermutations

class PostStatsOptions:
    def __init__(self, parent):
        self.parent = parent
        if "thresh" in self.parent.defaults:
            self.DEFAULT_THRESH = int(self.parent.defaults["thresh"])
        if "z_thresh" in self.parent.defaults:
            self.DEFAULT_Z_THRESH = float(self.parent.defaults["z_thresh"])
        if "prob_thresh" in self.parent.defaults:
            self.DEFAULT_PROB_THRESH = float(self.parent.defaults["prob_thresh"])
        if "rendertype" in self.parent.defaults:
            self.DEFAULT_RENDERTYPE = int(self.parent.defaults["rendertype"])
        if "zdisplay" in self.parent.defaults:
            self.DEFAULT_Z_DISPLAY = int(self.parent.defaults["zdisplay"])
        if "zmin" in self.parent.defaults:
            self.DEFAULT_ZMIN_RENDER = float(self.parent.defaults["zmin"])
        if "zmax" in self.parent.defaults:
            self.DEFAULT_ZMAX_RENDER = float(self.parent.defaults["zmax"])
        if "tsplot_yn" in self.parent.defaults:
            if int(self.parent.defaults["tsplot_yn"]) == 1:
                self.DEFAULT_TSPLOT = True
            else:
                self.DEFAULT_TSPLOT = False
    def Configure(self, thresh=None, zThresh=None, pThresh = None, renderType=None, zDisplay = None, zmin=None, zmax=None, makeTS = None, prethresholdMask = ""):
        """
        Configure post stats. Most of these options have to do with the rendering done of the results.
        :param thresh: (int) optional unless not specified in defaults. must be in FSFLabels.PostStatsThresholding.Options
        :param zThresh: (float) optional unless not specified in defaults
        :param pThresh: (float) optional unless not specified in defaults
        :param renderType: (int) optional unless not specified in defaults. must be FSFLabels.PostStatsColorRendering.Options
        :param zDisplay: (int) optional unless not specified in defaults. must be in FSFLabels.PostStatsZDisplay.Options
        :param zmin: (float) optional unless not specified in defaults.
        :param zmax: (float) optional unless not specified in defaults
        :param makeTS: (bool) optional unless not specified in defaults
        :return:
        """
        if thresh is None:
            if hasattr(self,'DEFAULT_THRESH'):
                thresh = self.DEFAULT_THRESH
            else:
                raise PyFSFError("No thresholding strategy was specified and none was found in defaults")
        else:
            if thresh not in PostStatsThresholding.Options:
                raise PyFSFError("Invalid thresholding strategy")
        self.parent.settings["thresh"] = thresh

        if zThresh is None:
            if hasattr(self, 'DEFAULT_Z_THRESH'):
                zThresh = self.DEFAULT_Z_THRESH
            else:
                raise PyFSFError("No Z threshold rendering type was specified and none was found in defaults")
        self.parent.settings["z_thresh"] = zThresh

        if pThresh is None:
            if hasattr(self, 'DEFAULT_PROB_THRESH'):
                pThresh = self.DEFAULT_PROB_THRESH
            else:
                raise PyFSFError("No prob threshold specified and none was found in defaults")
        self.parent.settings["prob_thresh"] = pThresh

        if renderType is None:
            if hasattr(self, 'DEFAULT_RENDERTYPE'):
                renderType = self.DEFAULT_RENDERTYPE
            else:
                raise PyFSFError("No render type was specified and non was found in defaults")
        else:
            if renderType not in PostStatsColorRendering.Options:
                raise PyFSFError("Invalid rendering type")
        self.parent.settings["rendertype"] = renderType

        if zDisplay is None:
            if hasattr(self, 'DEFAULT_Z_DISPLAY'):
                zDisplay = self.DEFAULT_Z_DISPLAY
            else:
                raise PyFSFError("No z display type was specified and non was found in defaults")
        else:
            if renderType not in PostStatsZDisplay.Options:
                raise PyFSFError("Invalid z display type")
        self.parent.settings["zdisplay"] = zDisplay

        if zmin is None:
            if hasattr(self, 'DEFAULT_Z_MIN'):
                zmin = self.DEFAULT_Z_MIN
            else:
                raise PyFSFError("No Z min for display was specified and none was found in defaults")
        self.parent.settings["zmin"] = zmin

        if zmax is None:
            if hasattr(self, 'DEFAULT_Z_MAX'):
                zmax = self.DEFAULT_Z_MAX
            else:
                raise PyFSFError("No Z max for display was specified and none was found in defaults")
        self.parent.settings["zmax"] = zmax

        if makeTS is None:
            if hasattr(self, 'DEFAULT_TSPLOT'):
                makeTS = self.DEFAULT_TSPLOT
            else:
                raise PyFSFError("No plot TS flag was specified and none was found in defaults")
        else:
            if makeTS not in [True, False]:
                raise PyFSFError("TS flag must be bool")
        self.parent.settings["tsplot_yn"] = int(makeTS)

        if prethresholdMask in ["", None]:
            self.parent.settings["threshmask"] = "\"\""
        else:
            try:
                str(prethresholdMask)
            except ValueError:
                raise PyFSFError("prethresholdMask must be str")
        self.parent.settings["threshmask"] = f"\"{prethresholdMask}\""

        # Set do post-stats flag to yes
        self.parent.settings["poststats_yn"] = 1
