setlocal

if [%ell_root%] == [] goto error

echo off
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
python cntk_import.py %model_path%\%model%.cntk.zip --zip_ell_model
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