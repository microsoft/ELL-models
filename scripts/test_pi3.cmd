setlocal
set ip_address=%1

call %~dp0test.cmd pi3 %ip_address% pi raspberry /home/pi

endlocal