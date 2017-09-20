setlocal
set ip_address=%1

call %~dp0test.cmd aarch64 %ip_address% linaro linaro /home/linaro

endlocal