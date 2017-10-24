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

REM optional cluster option for Raspberry Pi 3
if NOT [%6] == [] set cluster_option=--cluster %6

pushd ..
set "models_path=%cd%"
call :file_name_from_path models %models_path%
popd

set labels=categories.txt

pushd %ell_root%\build\tools\utilities\pitest
python drivetest.py --ipaddress %ip% --target %target% ^
  --labels %models_path%\%labels% --model %model_path%\%model%.ell.zip ^
  --username %username% --password %password% --target_dir %home%/test ^
  --profile %cluster_option%
popd

REM run_validation.py requires a one-time copy of validation set to %home%/validation
REM 
REM pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
REM python copy_validation_set.py z:\val_map.txt z:\images %ip% --maxfiles 50 ^
REM   --username=%username% --password=%password% --target_dir %home%/validation %cluster_option%
REM popd
REM

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python run_validation.py %model% %ip% --maxfiles 30 --labels %labels% ^
 --truth %home%/validation/val_map.txt --images %home%/validation --target %target% ^
 --username %username% --password %password% --target_dir %home%/test %cluster_option%

move test\%target%\validation.json %model_path%\validation_%target%.json
move test\%target%\validation.out %model_path%\validation_%target%.out
move test\%target%\procmon.json %model_path%\procmon_%target%.json
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