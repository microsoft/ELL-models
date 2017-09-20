setlocal

if [%ell_root%] == [] goto error
if [%5] == [] goto usage

echo off
set "model_path=%cd%"
call :file_name_from_path model %model_path%

set target=%1
set ip=%2
set username=%3
set password=%4
set home=%5

pushd ..
set "models_path=%cd%"
call :file_name_from_path models %models_path%
popd

set labels=%models%_labels.txt

pushd %ell_root%\build\tools\utilities\pitest
python drivetest.py %ip% --labels %models_path%\%labels% --model %model_path%\%model%.ell.zip --profile --target %target% ^
 --username %username% --password %password% --target_dir %home%/test
popd

REM run_validation.py requires a one-time copy of validation set to %home%/validation
REM 
REM pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
REM python copy_validation_set.py z:\val_map.txt z:\images %ip% --maxfiles 50 ^
REM   --username=%username% --password=%password% --target_dir %home%/validation
REM popd
REM

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python run_validation.py %model% %ip% --maxfiles 30 --labels %labels% ^
 --truth %home%/validation/val_map.txt --images %home%/validation --target %target% ^
 --username %username% --password %password% --target_dir %home%/test

move %model%_validation_%target%.json %model_path%\validation_%target%.json

move %model%_procmon_%target%.json %model_path%\procmon_%target%.json
popd
goto :done

:file_name_from_path <resultVar> <pathVar>
(
    set "%~1=%~nx2"
    exit /b
)

:usage
echo "%0 arch ip username password home_directory"
echo "e.g.: pi3 1.2.3.4 pi raspberry /home/pi"
goto :done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal