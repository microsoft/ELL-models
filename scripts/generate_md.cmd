setlocal

if [%ell_root%] == [] goto error

@echo off
set "model_path=%cd%"
call :file_name_from_path model %model_path%

if not exist modelargs.json echo "modelargs.json missing" && goto done

pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python generate_md.py %model_path% %ell_root%\docs\gallery\ILSVRC2012\%model%.md %ell_root%\build\bin\Release\print.exe
popd
goto done

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