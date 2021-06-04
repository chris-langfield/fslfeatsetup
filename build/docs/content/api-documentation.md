<a name="FSFLabels"></a>
# FSFLabels

<a name="FSF"></a>
# FSF

<a name="FSF.PyFSFError"></a>
## PyFSFError Objects

```python
class PyFSFError(Exception)
```

Generic error class for errors related to this module

<a name="FSF.FeatSettings"></a>
## FeatSettings Objects

```python
class FeatSettings()
```

<a name="FSF.FeatSettings.write"></a>
#### write

```python
 | write(path)
```

Collects all the configurations set by the child classes and writes out to an .fsf file.

**Arguments**:

- `path`: filepath to the .fsf file

**Returns**:

None

<a name="FSF.DataOptions"></a>
## DataOptions Objects

```python
class DataOptions()
```

Must be a child object of a FeatSettings instance.
This child must be created and configured before the others.

<a name="FSF.DataOptions.Configure"></a>
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

<a name="FSF.MiscOptions"></a>
## MiscOptions Objects

```python
class MiscOptions()
```

Must be a child object of a FeatSettings instance.

<a name="FSF.MiscOptions.Configure"></a>
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

<a name="FSF.PreStatsOptions"></a>
## PreStatsOptions Objects

```python
class PreStatsOptions()
```

<a name="FSF.PreStatsOptions.Configure"></a>
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



<a name="FSF.PreStatsOptions.Unwarping"></a>
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

<a name="EVs"></a>
# EVs

