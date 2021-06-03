# Test script and example of use
#
# Test data is not in repo but can be downloaded from:
# https://www.fmrib.ox.ac.uk/primers/intro_primer/ExBox11/IntroBox11.html


from FSF import *

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