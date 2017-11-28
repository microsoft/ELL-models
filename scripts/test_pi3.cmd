@echo off
setlocal

set ip_address=%1
set cluster_address=http://pidatacenter.cloudapp.net/api/values

call %~dp0test.cmd pi3 %ip_address% pi raspberry /home/pi %cluster_address%

endlocal