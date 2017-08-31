setlocal

set "model_path=%cd%"
call :file_name_from_path model %model_path%
set ell_root=c:\work\ELL

pushd %ell_root%\build\tools\importers\CNTK
python cntk_import.py %model_path%\%model%.cntk.zip --zip_ell_model
move %model_path%\%model%.ell.zip %model_path%\%model%.ell.zip
popd
goto :eof

:file_name_from_path <resultVar> <pathVar>
(
    set "%~1=%~nx2"
    exit /b
)

endlocal