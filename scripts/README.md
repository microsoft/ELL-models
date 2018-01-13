

## Importing models

```
python import_models.py --help

usage: This script imports CNTK models to ELL from a given search path

       [-h] [--path PATH]

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  the search path
```

- Run from any folder hierarchy containing *.cntk or *.cntk.zip.  The hierarchy can be anything because we do a glob on that file extension.

- Examples:
  - To import multiple models:
    ```
    set ell_root=<your_ell_root>
    cd <ELL-models>\models\ILSVRC2012 (or any folder structure with models)
    (py36) python <ELL-models>\scripts\import_models.py
    ```

  - To import any model:
    ```
    set ell_root=<your_ell_root>
    cd <ELL-models>\models\ILSVRC2012\dscs2_I128x128x3CCCCCCC1AS
    (py36) python <ELL-models>\scripts\import_models.py
    ```

## Testing models

```
python test_models.py --help                                                                   


usage: This script tests all ELL models found under a path, sequentially or in parallel.

       [-h] [--path PATH] [--parallel True] [--val_map file] [--val_set path]

optional arguments:
  -h, --help           show this help message and exit
  --path PATH          the model search path (or current directory if not specified)
  --parallel PARALLEL  test models in parallel (defaults to True)                                
  --labels LABELS      path to the labels file for evaluating the model                          
  --target {pi0,pi3}   the target platform                                                       
  --cluster CLUSTER    http address of the cluster server that controls access                   
                       to the target devices                                                     
  --val_set VAL_SET    path to the validation set images                                         
  --val_map VAL_MAP    path to the validation set truth                                          


```
- The tool searches the --path directory tree for *.ell.zip files and will test all of them.
- This calls [drivetest.py](https://github.com/Microsoft/ELL/blob/master/tools/utilities/pitest/drivetest.py) under the covers, 
and [run_validation.py](https://github.com/Microsoft/ELL/blob/master/tools/utilities/pythonlibs/gallery/run_validation.py) which 
executes the compiled model across a given validation set.
- If --parallel is True it uses dask.threaded to test models in parallel up to a maximum of 20 threads. If you run into any trouble with 
parallel execution of tests, you can always force the tests to run sequentially by setting --parallel False.

### VAL_MAP file 
This is a simple text file contains each image file name and the expected prediction that matches that image, like this:
```
  buffalo.png 346
  crocadile.png 49
  dungbeetle.png 305
  elephant.png 386
  hippo.png 344
  hyena.png 276
  impala.png 352
  leopard.png 293
  lion.png 291
  stork.png 43
  warthog.png 343
  wolf.jpeg 81
  zebra.png 340
```
### VAL_SET path

This path contains the images mentioned in the VAL_MAP file.  Using the above example, the folder should contain a file 
named "buffalo.png" as well as all the other images in that list.

### Examples
    Assuming you have the following environment variables defined:

    set ell_root=<your_ell_root>
    set cluster=<your test machine cluster web service>
    set images=<path to your test images>

  - To test multiple models in parallel:
    ```
    cd <ELL-models>\models\ILSVRC2012 (or any folder structure containing multiple models)
    (py36) python <ELL-models>\scripts\test_models.py --cluster %cluster% --val_map %images%\val_map.txt --val_set %images%
    ```

  - To test a single model:
    ```
    (py36) python <ELL-models>\scripts\test_model.py --cluster %cluster% -val_map %images%\val_map.txt --val_set %images%
    ```

  - To test multiple models, sequentially:
    ```
    (py36) python <ELL-models>\scripts\test_models.py --cluster %cluster% --val_map %images%\val_map.txt --val_set %images% --parallel False
    ```
  
  - To move the temp files created by this process out of the ELL-models location, use the --path variable:
  
    ```
    cd d:\temp\foo
    (py36) python <ELL-models>\scripts\test_models.py --cluster %cluster% --val_map %images%\val_map.txt --val_set %images% --path <ELL-models>\models\ILSVRC2012
    ```

### Cluster Web Service

Your cluster web service manages the locking and unlocking of test machines.  Your service must implement the
[picluster.py](https://github.com/Microsoft/ELL/blob/master/tools/utilities/pythonlibs/picluster.py) API which 
is a simple RESTful web service that makes it possible to centrally get/lock/unlock machines so that multiple
people in your group can share the same pool of test machines.  