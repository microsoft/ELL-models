@echo off
setlocal enabledelayedexpansion

if [%1] == [] goto usage
if [%2] == [] (set models_subdirectory="ILSVRC2012") else (set models_subdirectory=%2)
if [%3] == [] goto usage
if [%4] == [] goto usage

set rpi_ip_address=%1
set rpi_64_ip_address=%3
set dragonboard_ip_address=%4

if [%ell_root%] == [] goto error

set labels=categories.txt

REM traverse all models in the ILSVRC2012 directory
for /f %%f in ('dir /ad /b ..\models\%models_subdirectory%\*_*') do (
    echo %models_subdirectory%
    pushd ..\models\%models_subdirectory%\%%f
    ..\..\..\scripts\import.cmd
    popd
    REM run validation on Raspberry Pi 3 / Raspbian
    pushd ..\models\%models_subdirectory%\%%f
    ..\..\..\scripts\test_pi3.cmd %rpi_ip_address%
    popd
    REM run validation on Raspberry Pi 3 / OpenSUSE
    pushd ..\models\%models_subdirectory%ILSVRC2012\%%f
    ..\..\..\scripts\test_pi3_64.cmd %rpi_64_ip_address%
    popd
    REM REM run validation on Dragonboard
    pushd ..\models\%models_subdirectory%\%%f
    ..\..\..\scripts\test_aarch64.cmd %dragonboard_ip_address%
    popd
    REM generate the markdown file
    pushd ..\models\%models_subdirectory%\%%f
    ..\..\..\scripts\generate_md.cmd
    popd
)

REM plot pareto curves to select the best models
pushd ..\models\%models_subdirectory%
..\..\scripts\plot_pareto.cmd
popd

goto done

:usage
echo "Usage: %0 raspberry_pi_ip_address models_subdirectory opensuse_ip_address dragonboard_ip_address"
goto done

:error
echo "ell_root not set, please set it to the root of your ELL repository"

:done
endlocal