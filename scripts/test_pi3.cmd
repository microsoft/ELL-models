setlocal

if [%ell_root%] == [] goto error

echo off
set "model_path=%cd%"
call :file_name_from_path model %model_path%
set ip=%1
set labels=%2

pushd ..
set "models_path=%cd%"
call :file_name_from_path models %models_path%
popd

if [%2] == [] set labels=%models%_labels.txt

pushd %ell_root%\build\tools\utilities\pitest
python drivetest.py %ip% --labels %models_path%\%labels% --model %model_path%\%model%.ell.zip --profile --target pi3
popd

REM Assumes one-time copy of validation set to /home/pi/validation
REM 
REM pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
REM python copy_validation_set.py z:\val_map_original.txt z:\images %ip% --maxfiles 50
REM popd
REM

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python run_validation.py %model% %ip% --maxfiles 30 --labels %labels%
move %model%_validation_pi3.json %model_path%\validation_pi3.json
move %model%_procmon_pi3.json %model_path%\procmon_pi3.json
popd
goto :done

:file_name_from_path <resultVar> <pathVar>
(
    set "%~1=%~nx2"
    exit /b
)

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal