setlocal

if [%ell_root%] == [] goto error

set "model_path=%cd%"
call :file_name_from_path model %model_path%

REM zip up the CNTK model
REM pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
REM python zip_file.py %model_path%\%model%.cntk
REM popd

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