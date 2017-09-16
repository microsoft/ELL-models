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
python drivetest.py %ip% --labels %models_path%\%labels% --model %model_path%\%model%.ell.zip --profile --target pi3_64 --username root --password linux --target_dir /root/test
popd

REM Assumes one-time copy of validation set to /home/pi/validation
REM 
REM pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
REM python copy_validation_set.py z:\val_map_original.txt z:\images %ip% --maxfiles 50
REM popd
REM

REM pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
REM python run_validation.py %model% %ip% --maxfiles 30 --labels %labels% --truth /home/linaro/validation/val_map_original.txt --images /root/validation --target pi3_64 --username root --password linux --target_dir /root/test
REM move %model%_validation_pi3_64.json %model_path%\validation_pi3_64.json
REM move %model%_procmon_pi3_64.json %model_path%\procmon_pi3_64.json
REM popd
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