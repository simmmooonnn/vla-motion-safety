@echo off
if not exist "E:\ovhome" mkdir "E:\ovhome"
if not exist "E:\ovtmp"  mkdir "E:\ovtmp"
if not exist "E:\ovwarp" mkdir "E:\ovwarp"
set "LOCALAPPDATA=E:\ovhome"
set "TEMP=E:\ovtmp"
set "TMP=E:\ovtmp"
set "WARP_CACHE_PATH=E:\ovwarp"
call "E:\Isaac\isaac\python.bat" "%~dp0scripts\probe_api.py"
pause
