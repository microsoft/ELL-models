setlocal enabledelayedexpansion
echo off

if [%1] == [] goto usage
if [%2] == [] goto usage
if [%3] == [] goto usage

set rpi_ip_address=%1
set rpi_64_ip_address=%2
set dragonboard_ip_address=%3

if [%ell_root%] == [] goto error

set labels=categories.txt

REM traverse all models in the ILSVRC2012 directory
for /f %%f in ('dir /ad /b ..\models\ILSVRC2012\*_*') do (
    pushd ..\models\ILSVRC2012\%%f
    REM ..\..\..\scripts\import.cmd
    popd
    REM run validation on Raspberry Pi 3 / Raspbian
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\test_pi3.cmd %rpi_ip_address%
    popd
    REM run validation on Raspberry Pi 3 / OpenSUSE
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\test_pi3_64.cmd %rpi_64_ip_address%
    popd
    REM run validation on Dragonboard
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\test_aarch64.cmd %dragonboard_ip_address%
    popd
    REM generate the markdown file
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\generate_md.cmd
    popd
)

REM plot pareto curves to select the best models
pushd ..\models\ILSVRC2012
..\..\scripts\plot_pareto.cmd
popd

goto done

:usage
echo "Usage: %0 raspberry_pi_ip_address opensuse_ip_address dragonboard_ip_address"
goto done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal