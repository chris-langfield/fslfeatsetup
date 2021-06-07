# Test script and example of use
#
# Test data is not in repo but can be downloaded from:
# https://www.fmrib.ox.ac.uk/primers/intro_primer/ExBox11/IntroBox11.html

import glob
from FSF import *

def TestFirstLevel():

    outputDir = "test.feat"
    inputs = ["sampledata/ExBox11/fmri.nii.gz"]
    structural = ["sampledata/ExBox11/structural_brain.nii.gz"]


    simpleRunFSF = FeatSettings(FeatLevel.FIRST_LEVEL, FeatAnalysis.FULL_ANALYSIS)

    srData = DataOptions(simpleRunFSF)
    srData.Configure(outputDir, inputs, highPassCutoff=70)
    srData.printSettings()

    srMisc = MiscOptions(simpleRunFSF)
    srMisc.Configure(brainThreshold=10, zThreshold=2.3)
    srMisc.printSettings()

    srPreStats = PreStatsOptions(simpleRunFSF)
    srPreStats.Configure(mcflirt=True, b0_unwarp=False, melodic=False, sliceTiming=FeatSliceTiming.REGULAR_UP, bet=True)

    srReg = RegOptions(simpleRunFSF)
    srReg.ConfigureMainStructural(structural)

    simpleRunFSF.printSettings()

    srStats = StatsOptions(simpleRunFSF)

    srStats.AddFirstLevelEV("bla","bla.txt", Gamma(0,7,1))
    srStats.OrthogonalizeEVs([[1,0],[0,1]])

    simpleRunFSF.write("testfirstlevl.fsf")

def TestHigherLevel():
    outputDir = "testHigherLevel.gfeat"
    inputs = glob.glob("sampledata/ExBox*/fmri.feat/stats/cope1.nii.gz")

    simpleHigherLevel = FeatSettings(FeatLevel.HIGHER_LEVEL, FeatAnalysis.STATS)
    shlData = DataOptions(simpleHigherLevel)
    shlData.Configure(outputDir, inputs, higherLevelInput=FeatHigherLevelInput.COPE_IMAGES)
    shlMisc = MiscOptions(simpleHigherLevel)
    shlMisc.Configure(cleanupFirstLevel=True)
    shlStats = StatsOptions(simpleHigherLevel)
    shlStats.AddHigherLevelEV("sub1", [1.0,0])
    shlStats.AddHigherLevelEV("sub2", [0,1.0])
    shlStats.AddContrast("sub1-sub2", [1.0,-1.0])
    orthoMatrix = [[ 0 for x in range(len(inputs)+1)] for y in range(len(inputs)+1)]
    shlStats.OrthogonalizeEVs(orthoMatrix)

    simpleHigherLevel.write("testhigherlevel.fsf")

TestHigherLevel()
TestFirstLevel()

