@echo off
setlocal

if [%ell_root%] == [] goto error

set "model_path=%cd%"
call :file_name_from_path model %model_path%

REM zip up the CNTK model
if exist %model_path%\%model%.cntk (
    pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
    python zip_file.py %model_path%\%model%.cntk
    popd
)

REM convert the CNTK model to ELL
pushd %ell_root%\build\tools\importers\CNTK
python cntk_import.py %model_path%\%model%.cntk --zip_ell_model
popd

REM rename some training-generated files to shorter names
if exist %model%_args.json move %model%_args.json args.json
if exist %model%_modelargs.json move %model%_modelargs.json modelargs.json

goto :done

:file_name_from_path <resultVar> <pathVar>
(
    for  %%x in (*.cntk) do (
        SET "%~1=%%~nx"
        exit /b
    )
)

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal