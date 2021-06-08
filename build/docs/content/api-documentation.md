<a name="fslfeatsetup"></a>
# fslfeatsetup

<a name="fslfeatsetup.FSFLabels"></a>
# fslfeatsetup.FSFLabels

<a name="fslfeatsetup.FSF"></a>
# fslfeatsetup.FSF

<a name="fslfeatsetup.FSF.PyFSFError"></a>
## PyFSFError Objects

```python
class PyFSFError(Exception)
```

Generic error class for errors related to this module

<a name="fslfeatsetup.FSF.FeatSettings"></a>
## FeatSettings Objects

```python
class FeatSettings()
```

<a name="fslfeatsetup.FSF.FeatSettings.write"></a>
#### write

```python
 | write(path)
```

Collects all the configurations set by the child classes and writes out to an .fsf file.

**Arguments**:

- `path`: filepath to the .fsf file

**Returns**:

None

<a name="fslfeatsetup.FSF.DataOptions"></a>
## DataOptions Objects

```python
class DataOptions()
```

Must be a child object of a FeatSettings instance.
This child must be created and configured before the others.

<a name="fslfeatsetup.FSF.DataOptions.Configure"></a>
#### Configure

```python
 | Configure(outputDirectory, inputPaths, totalVolumes=-1, deleteVolumes=-1, tr=-1, highPassCutoff=-1, higherLevelInput=FeatHigherLevelInput.COPE_IMAGES)
```

Takes parameters corresponding to the "Data" tab in the FEAT GUI. It then updates the settings list of its FeatSettings parent class.

**Arguments**:

- `outputDirectory`: Mandatory .feat or .gfeat path
- `inputPaths`: Mandatory list of input filepaths
- `totalVolumes`: Optional number of volumes per input. Can be inferred if left blank.
- `deleteVolumes`: Optional number of volumes to delete. Will be set to default found in defaults file, or otherwise set to 0
- `tr`: Optional TR of input images. Can be inferred if left blank.
- `highPassCutoff`: Optional, unless default file does not contain this setting
- `higherLevelInput`: Optional, for higher-level analyses only. Can be set to 1 (lower-level feat directories) or 2 (lower level cope images), or using the built-in type FeatHigherLevelInput.FEAT_DIRS or FeatHigherLevelInput.COPE_IMAGES

**Returns**:

None

<a name="fslfeatsetup.FSF.MiscOptions"></a>
## MiscOptions Objects

```python
class MiscOptions()
```

Must be a child object of a FeatSettings instance.

<a name="fslfeatsetup.FSF.MiscOptions.Configure"></a>
#### Configure

```python
 | Configure(brainThreshold=-1, noiseLevel=-1, temporalSmoothness=-1, zThreshold=-1, cleanupFirstLevel=None, overwriteOriginalPostStats=None, estimateNoiseFromData=False)
```

Takes parameters corresponding to the "Misc" tab in the FEAT GUI. It then updates the settings list of its FeatSettings parent class.

**Arguments**:

- `brainThreshold`: Optional unless not specified in defaults file
- `noiseLevel`: Optional unless not specified in defaults file
- `temporalSmoothness`: Optional unless not specified in defaults file
- `zThreshold`: Optional unless not specified in defaults file
- `cleanupFirstLevel`: Optional unless not specified in defaults file
- `overwriteOriginalPostStats`: Optional unless not specified in defaults file
- `estimateNoiseFromData`: TODO

**Returns**:

None

<a name="fslfeatsetup.FSF.PreStatsOptions"></a>
## PreStatsOptions Objects

```python
class PreStatsOptions()
```

<a name="fslfeatsetup.FSF.PreStatsOptions.Configure"></a>
#### Configure

```python
 | Configure(mcflirt=None, b0_unwarp=None, melodic=None, sliceTiming=None, sliceTimingFile=None, bet=None, spatialSmoothing=-1.0, intensityNormalization=None, perfusionSubtraction=None, perfusionTagControlOrder=None, highPassTemporalFilter=None, lowPassTemporalFilter=None, usingAlternateReferenceImage=None, alternateReferenceImages=None)
```

Takes parameters corresponding to the "Pre-stats" tab in the FEAT GUI. It then updates the settings list of its FeatSettings parent class.

**Arguments**:

- `mcflirt`: Optional unless not specified in defaults file
- `b0_unwarp`: Optional unless not specified in defaults file
- `melodic`: Optional unless not specified in defaults file
- `sliceTiming`: Optional, defaults to 0
- `sliceTimingFile`: Mandatory depending on `sliceTiming`
- `bet`: Optional unless not specified in defaults file
- `spatialSmoothing`: Optional unless not specified in defaults file
- `intensityNormalization`: Optional unless not specified in defaults file
- `perfusionSubtraction`: Optional unless not specified in defaults file
- `perfusionTagControlOrder`: Optional unless not specified in defaults file
- `highPassTemporalFilter`: Optional unless not specified in defaults file
- `lowPassTemporalFilter`: Optional unless not specified in defaults file
- `usingAlternateReferenceImage`: Optional unless not specified in defaults file
- `alternateReferenceImages`: Mandatory list of images, one per input, if `usingAlternateReferenceImage` is true

**Returns**:



<a name="fslfeatsetup.FSF.PreStatsOptions.Unwarping"></a>
#### Unwarping

```python
 | Unwarping(fieldmapImages, fieldmapMagnitudeImages, epiDwell=None, epiTE=None, unwarpDir=None, signalLoss=None)
```

Optionally sets up the B0 Unwarping fields. Must have already run `Configure()`

**Arguments**:

- `fieldmapImages`: Mandatory list of images, one for each input
- `fieldmapMagnitudeImages`: Mandatory list of images, one for each input
- `epiDwell`: Optional unless not specified in defaults file
- `epiTE`: Optional unless not specified in defaults file
- `unwarpDir`: Optional unless not specified in defaults file
- `signalLoss`: Optional unless not specified in defaults file

**Returns**:

None

<a name="fslfeatsetup.FSF.StatsOptions"></a>
## StatsOptions Objects

```python
class StatsOptions()
```

<a name="fslfeatsetup.FSF.StatsOptions.Configure"></a>
#### Configure

```python
 | Configure(preWhitening=None)
```

Configure the Stats settings.

**Arguments**:

- `preWhitening`: (bool) optional unless not specified in defaults

**Returns**:

None

<a name="fslfeatsetup.FSF.StatsOptions.ConfigureHigherLevel"></a>
#### ConfigureHigherLevel

```python
 | ConfigureHigherLevel(model=None, outlierDeweighting=None, randomisePermutations=None)
```

Configure higher level options

**Arguments**:

- `model`: (int) must be FSFLabels.HigherLevelModeling.Options
- `outlierDeweighting`: (bool) optional unless not specified in defaults
- `randomisePermutations`: (int) optional unless not specified in defaults

**Returns**:



<a name="fslfeatsetup.FSF.PostStatsOptions"></a>
## PostStatsOptions Objects

```python
class PostStatsOptions()
```

<a name="fslfeatsetup.FSF.PostStatsOptions.Configure"></a>
#### Configure

```python
 | Configure(thresh=None, zThresh=None, pThresh=None, renderType=None, zDisplay=None, zmin=None, zmax=None, makeTS=None)
```

Configure post stats. Most of these options have to do with the rendering done of the results.

**Arguments**:

- `thresh`: (int) optional unless not specified in defaults. must be in FSFLabels.PostStatsThresholding.Options
- `zThresh`: (float) optional unless not specified in defaults
- `pThresh`: (float) optional unless not specified in defaults
- `renderType`: (int) optional unless not specified in defaults. must be FSFLabels.PostStatsColorRendering.Options
- `zDisplay`: (int) optional unless not specified in defaults. must be in FSFLabels.PostStatsZDisplay.Options
- `zmin`: (float) optional unless not specified in defaults.
- `zmax`: (float) optional unless not specified in defaults
- `makeTS`: (bool) optional unless not specified in defaults

**Returns**:



<a name="fslfeatsetup.EVs"></a>
# fslfeatsetup.EVs

<a name="fslfeatsetup.EVs.FeatEVShapes"></a>
## FeatEVShapes Objects

```python
class FeatEVShapes()
```

Enum specifying all the options for a first-level EV. Used for the shape kwarg in the constructor of the FirstLevelEV class
Only Custom3Column currently enabled

<a name="fslfeatsetup.EVs.FeatHRFConvolution"></a>
## FeatHRFConvolution Objects

```python
class FeatHRFConvolution()
```

Enum specifying the types of HRF convolutions for a first level EV. Possibly unneeded.

<a name="fslfeatsetup.EVs.Gamma"></a>
## Gamma Objects

```python
class Gamma()
```

Object representing a Gamma convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.

<a name="fslfeatsetup.EVs.DoubleGamma"></a>
## DoubleGamma Objects

```python
class DoubleGamma()
```

Object representing a Double Gamma convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.

<a name="fslfeatsetup.EVs.AltDoubleGamma"></a>
## AltDoubleGamma Objects

```python
class AltDoubleGamma()
```

Object representing an Alternate Double Gamma convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.

<a name="fslfeatsetup.EVs.Gaussian"></a>
## Gaussian Objects

```python
class Gaussian()
```

Object representing a Gaussian convolution and its parameters. Used for the hrf kwarg in the FirstLevelEV class.

<a name="fslfeatsetup.EVs.FirstLevelEV"></a>
## FirstLevelEV Objects

```python
class FirstLevelEV()
```

Object representing a first level EV. Will be refactored.

<a name="fslfeatsetup.EVs.HigherLevelEV"></a>
## HigherLevelEV Objects

```python
class HigherLevelEV()
```

Object representing a higher level EV

<a name="fslfeatsetup.EVs.Contrast"></a>
## Contrast Objects

```python
class Contrast()
```

Object representing a contrast

<a name="fslfeatsetup.Comments"></a>
# fslfeatsetup.Comments

