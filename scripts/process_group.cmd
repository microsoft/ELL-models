setlocal enabledelayedexpansion
echo off

set rpi_ip_address=%1

if [%ell_root%] == [] goto error

for /f %%f in ('dir /ad /b ..\models\ILSVRC2012\d_*') do (
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\import.cmd
    popd
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\test.cmd %rpi_ip_address%
    popd
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\generate_md.cmd
    popd
)

REM generate the gallery index file
pushd %ell_root%\build\tools\utilities\pythonlibs\gallery
python generate_index.py %ell_root%\docs\gallery\ILSVRC2012
popd

goto done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal