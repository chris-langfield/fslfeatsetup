Temporary documentation

### class: DataOptions

`Configure(str outputDirectory, str[] inputPaths, int totalVolumes=-1, int deleteVolumes=-1, int tr=-1, int highPassCutoff=-1, FeatHigherLevelInput higherLevelInput=COPE_IMAGES)`

### class: MiscOptions

`Configure(int brainThreshold=-1, int noiseLevel=-1, int temporalSmoothness=-1, int zThreshold=-1, bool cleanUpFirstLevel=None, estimateNoiseFromData=False)`

### class: PreStatsOptions

`Configure(bool mcflirt=None, bool b0_unwarp=None, bool melodic=None, FeatSliceTiming sliceTiming=None, str sliceTimingFile=None, bool bet=None, float spatialSmoothing=-1.0, bool intensityNormalization=None, bool perfusionSubtraction=None, FeatPerfusion perfusionTagControlOrder=-1, bool highPassTemporalFilter=None, bool lowPassTemporalFilter=None, bool usingAlternateReferenceImage=None, str[] alternateReferenceImages=None)`

`Unwarping(str[] fieldmapImages, str[] fieldmapMagnitudeImages, float epiDwell=None, float epiTE=None, FeatUnwarp unwarpDir=None, int signalLoss=None)`

### class: RegOptions

`ConfigureMainStructural(str[] mainStructuralImages, RegistrationSearch mainStructuralRegSearch=None, RegistrationDOF mainStructuralDOF=None)`

`ConfigureExpandedFunctional(str[] expandedFunctionalImages, RegistrationSearch expandedFunctionalSearch=None, RegistrationDOF expandedFunctionalDOF=None)`

`ConfigureStandardSpace(str standardImage=None, RegistrationSearch standardSearch=None, RegistrationDOF standardDOF=None, bool doNonLinear=None, int warpResolution=None)`

