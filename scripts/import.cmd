setlocal

set "model_path=%cd%"
call :file_name_from_path model %model_path%
set ell_root=c:\work\ELL

REM zip up the CNTK model
pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python zip_file.py %model_path%\%model%.cntk
popd

REM convert the CNTK model to ELL
pushd %ell_root%\build\tools\importers\CNTK
python cntk_import.py %model_path%\%model%.cntk.zip --zip_ell_model
popd
goto :eof

:file_name_from_path <resultVar> <pathVar>
(
    set "%~1=%~nx2"
    exit /b
)

endlocal