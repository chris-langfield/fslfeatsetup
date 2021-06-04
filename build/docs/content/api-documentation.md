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

Must be a child object of a FeatSettings instance
This child must be created and configured before the others

<a name="FSF.DataOptions.Configure"></a>
#### Configure

```python
 | Configure(outputDirectory, inputPaths, totalVolumes=-1, deleteVolumes=-1, tr=-1, highPassCutoff=-1, higherLevelInput=FeatHigherLevelInput.COPE_IMAGES)
```

Takes parameters corresponding to the "Data" tab in the FEAT GUI. It then updates the settings list of its FeatSettings parent class.

**Arguments**:

or using the built-in type FeatHigherLevelInput.FEAT_DIRS or FeatHigherLevelInput.COPE_IMAGES
- `outputDirectory`: Mandatory .feat or .gfeat path
- `inputPaths`: Mandatory list of input filepaths
- `totalVolumes`: Optional number of volumes per input. Can be inferred if left blank.
- `deleteVolumes`: Optional number of volumes to delete. Will be set to default found in defaults file, or otherwise set to 0
- `tr`: Optional TR of input images. Can be inferred if left blank.
- `highPassCutoff`: Optional, unless default file does not contain this setting
- `higherLevelInput`: Optional, for higher-level analyses only. Can be set to 1 (lower-level feat directories) or 2 (lower level cope images),

**Returns**:

None

<a name="EVs"></a>
# EVs

