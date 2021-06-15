![devstatus](https://img.shields.io/badge/development--status-alpha-yellowgreen) ![pypi_badge](https://img.shields.io/pypi/v/fslfeatsetup?style=plastic)

# fslfeatsetup
 
Python functions to create an FSL FEAT configuration file (.fsf)

Can be run from python command line/REPL or incorporated into a script

**Alpha version available on PyPI**

```pip install fslfeatsetup```

Feel free to contribute

[DOCUMENTATION](build/docs/content/api-documentation.md) generated by [pydoc-markdown](https://github.com/NiklasRosenstein/pydoc-markdown)

[On Python Package Index](https://pypi.org/project/fslfeatsetup/)

## Overview

The .fsf file is represented by the class `FeatSettings`, which is constructed with the analysis level and analysis type options.

![featoptions](https://user-images.githubusercontent.com/34426450/121554571-4278c380-c9e0-11eb-8c9b-51b99588cad8.png)

Each panel of the FEAT GUI is represented by a separate class, taking the initial `FeatSettings` object as its argument. Each of these objects has a `Configure()` function taking keyword arguments specifying the options available in that panel of the GUI. These are the `MiscOptions`, `DataOptions`, `PreStatsOptions`, `RegOptions`, `StatsOptions`, and `PostStatsOptions` classes.

For example the checkboxes and inputs on the Misc Options GUI panel correspond to the key-word arguments in the `MiscOptions.Configure()` function.

`MiscOptions.Configure(brainThreshold=10, noiseLevel=0.66, temporalSmoothness=0.05, zThreshold=5.3, cleanupFirstLevel=False, overwriteOriginalPostStats = False, estimateNoiseFromData=False)`
                 
(*Some of these options pertain only to higher-level analyses*)


![featmisc](https://user-images.githubusercontent.com/34426450/121555239-d3e83580-c9e0-11eb-97b8-a1a15861aa5d.png)

Dropdown lists are represented by enum-like classes:

`PreStatsOptions.Configure(st = FeatSliceTiming.REGULAR_UP)`

`PreStatsOptions.Configure(st = FeatSliceTiming.TIMING_FILE, sliceTimingFile = "path/to/file")`

![featdropdown](https://user-images.githubusercontent.com/34426450/121556252-b798c880-c9e1-11eb-8bae-a9058501d2bf.png)



## First-level analysis example
```python
    from fslfeatsetup.FSF import *
    from fslfeatsetup.EVs import *
    from fslfeatsetup.FSFLabels import *

    SubjectFMRI = [ ... ] 
    SubjectStructurals = [ ... ]

    for i in range(len(SubjectFMRI)):
           # initialize the FeatSettings object
           FSF = FeatSettings(FeatLevel.FIRST_LEVEL, FeatAnalysis.FULL_ANALYSIS)
           
           # Configure the Data options
           Data = DataOptions(FSF)
           # The only required inputs are the output FEAT directory, and the list of 
           # FMRI files (or lower-level feats, see Higher Level Analysis example
           Data.Configure("path/to/output/subject_i",[SubjectFMRI[i]])

           # Configure the Miscellaneous options
           Misc = MiscOptions(FSF)
           # There are NO required inputs. Using the defaults specified in my FSL installation. 
           # If fslfeatsetup needs an option that is not in the defaults, it will let you know 
           Misc.Configure()

           # Configure Registration options
           Reg = RegOptions(FSF)
           
           # I can specify a standard to use, or I can go with the default 2mm MNI152, as I am here
           Reg.ConfigureStandardSpace()
           # The only required argument 
           Reg.ConfigureMainStructural([SubjectStructurals[i]])
           
           # If I don't want to use expanded functional data, I simply don't configure it
           # Reg.ConfigureExpandedFunctional([ this would be a list of your expanded functional images ])
           
           
           # Configure Pre-Stats options
           PreStats = PreStatsOptions(FSF)
           # The library has built-in enum-like structures that hardcode the FEAT options
           PreStats.Configure(sliceTiming=FeatSliceTiming.TIMING_FILE,
                                 sliceTimingFile="path/to/slice/timing/file",
                                 bet=True)
                                 
           # Configure Stats options
           Stats = StatsOptions(FSF)
           # using all defaults, so I don't need to specify keyword arguments
           Stats.Configure()
           # Add EVs from custom 3 column text formats. 
           # Note that ONLY the 3-column text file format is currently supported
           # specify the parameters of the convolution function, or use defaults
           Stats.AddFirstLevelEV("myEV1","path/to/my/EV1",Gamma(phase=0, stdev=3, lag=6))
           Stats.AddFirstLevelEV("myEV2","path/to/my/EV2",Gamma())
           Stats.AddFirstLevelEV("myEV3","path/to/my/EV3",Gamma())

           # orthogonalize
           # The argument is a pythonic matrix (list of lists)
           # the size of this matrix will be one larger than the number of EVs
           Stats.OrthogonalizeEVs([ [ 0 for x in range(4)] for y in range(4)])

           # Configure Post-Stats options
           PostStats = PostStatsOptions(FSF)
           # using all defaults except for min and max Z-threshold for rendering
           PostStats.Configure(zmin = 2, zmax= 8)

           # write to .fsf file
           FSF.write("path/to/subject_i/fsf")

```

## Higher-level analysis steps

todo

## Changelog

|  PyPI version |  Description |
| ------ | ------ |
| 0.2.8  | Generated an .fsf accepted by FEAT. There are a bunch of hard-coded defaults that still need to be fixed |
| 0.2.5  | Fixed gammadelay being blank and FSLDIR not found |
| 0.2.3  | Patch: quotations for custom EV files |
| 0.2.1  | Patched a silly bug |
| 0.2.0  | first "complete" version, with post-stats options and auto generated comments. still very much a work in progress |
| 0.1.2  | first stable version - package still a work in progress |
