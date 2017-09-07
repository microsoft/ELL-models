setlocal

if [%ell_root%] == [] goto error

echo off
set "model_path=%cd%"
call :file_name_from_path model %model_path%

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python generate_md.py %model_path% %model_path%\%model%.md
move %model_path%\%model%.md %ell_root%\docs\gallery\ILSVRC2012
popd
goto done

:file_name_from_path <resultVar> <pathVar>
(
    set "%~1=%~nx2"
    exit /b
)

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal