setlocal
set ip_address=%1

call %~dp0test.cmd pi3_64 %ip_address% root linux /root

endlocal