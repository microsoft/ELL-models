

## Importing models

```
import_models.py

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
                                                                                                 
       [-h] [--path PATH] [--parallel PARALLEL] [--labels LABELS]                                
       [--target {pi0,pi3}] [--cluster CLUSTER] [--val_set VAL_SET]                              
       [--val_map VAL_MAP]                                                                       
                                                                                                 
optional arguments:                                                                              
  -h, --help           show this help message and exit                                           
  --path PATH          the model search path (or current directory if not                        
                       specified)                                                                
  --parallel PARALLEL  test models in parallel (defaults to True)                                
  --labels LABELS      path to the labels file for evaluating the model                          
  --target {pi0,pi3}   the target platform                                                       
  --cluster CLUSTER    http address of the cluster server that controls access                   
                       to the target devices                                                     
  --val_set VAL_SET    path to the validation set images                                         
  --val_map VAL_MAP    path to the validation set truth                                          
                                                                                                 
```
- Run from any folder hierarchy containing *.ell.zip.  The hierarchy can be anything because we do a glob on that file extension.
- This calls drivetest.py under the covers, and another test called run_validation.py that executes across the validation set.
- By default this uses dask.threaded to test models in parallel. If you run into any trouble with parallel execution of tests, you can always force the tests to run sequentially by setting --parallel False

- Setup
  - Map the Y drive (or any drive to the validation set), like this:
    ```
    Directory of Y:\

        XX/XX/2017  05:13 PM    <DIR>          .
        XX/XX/2017  12:20 PM    <DIR>          ..
        XX/XX/2017  03:43 PM         2,044,500 val_map.txt
        XX/XX/2017  05:46 PM    <DIR>          images
    ```

- Examples
  - To test multiple models:
    ```
    set ell_root=<your_ell_root>
    cd <ELL-models>\models\ILSVRC2012 (or any folder structure with models)
    (py36) python <ELL-models>\scripts\test_models.py --cluster CLUSTER_IP --val_set Y:\images --val_map Y:\images\val_map.txt
    ```

  - To test any model:
    ```
    set ell_root=<your_ell_root>
    cd <ELL-models>\models\ILSVRC2012\dscs2_I128x128x3CCCCCCC1AS
    (py36) python <ELL-models>\scripts\test_models.py --cluster CLUSTER_IP --val_set Y:\images --val_map Y:\images\val_map.txt
    ```

  - To test multiple models, sequentially:
    ```
    set ell_root=<your_ell_root>
    cd <ELL-models>\models\ILSVRC2012 (or any folder structure with models)
    (py36) python <ELL-models>\scripts\test_models.py --parallel False  --cluster CLUSTER_IP --val_set Y:\images --val_map Y:\images\val_map.txt
    ```
