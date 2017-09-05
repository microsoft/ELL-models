REM Usage: process_group 160 ip_address
setlocal enabledelayedexpansion

for /f %%f in ('dir /ad /b ..\models\ILSVRC2012\d_I%1*') do (
    pushd ..\models\ILSVRC2012\%%f
    ..\..\..\scripts\import.cmd
    ..\..\..\scripts\test.cmd %2
    REM ..\..\..\scripts\generate_md.cmd
    popd
)

endlocal