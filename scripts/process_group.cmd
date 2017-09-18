setlocal enabledelayedexpansion
echo off

if [%1] == [] goto usage
if [%2] == [] goto usage
if [%3] == [] goto usage

set rpi_ip_address=%1
set rpi_64_ip_address=%2
set dragonboard_ip_address=%3

if [%ell_root%] == [] goto error

set labels=ILSVRC2012_labels.txt

for /f %%f in ('dir /ad /b ..\models\ILSVRC2012\d_I160x160x3CMCMCMCMCMCMC1A*') do (
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\import.cmd
    popd
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\test_pi3.cmd %rpi_ip_address%
    popd
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\test_pi3_64.cmd %rpi_64_ip_address%
    popd
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\test_aarch64.cmd %dragonboard_ip_address%
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

:usage
echo "Usage: %0 raspberry_pi_ip_address opensuse_ip_address dragonboard_ip_address"
goto done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal