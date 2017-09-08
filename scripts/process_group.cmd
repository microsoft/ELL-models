REM Usage: process_group 160 ip_address
setlocal enabledelayedexpansion
echo off

if [%ell_root%] == [] goto error

for /f %%f in ('dir /ad /b ..\models\ILSVRC2012\d_I%1*') do (
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\import.cmd
    ..\..\..\scripts\test.cmd %2
    ..\..\..\scripts\generate_md.cmd
    popd
)
goto done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal