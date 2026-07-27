@echo off
REM ============================================================
REM  WATCH the "aware" condition with a 3D viewport.
REM  The planner knows about the hazard capsule, so the arm should
REM  steer around it on its way from A to B.
REM
REM  This is for watching, not for producing the official numbers -
REM  it writes to results\watch_aware.* so it will not overwrite the
REM  verified results\aware.* files. Use run_experiment.bat for data.
REM
REM  Rendering on a 4 GB GPU is slower than headless. Expect the
REM  window to take 1-2 minutes to appear while Isaac starts up.
REM
REM  NOTE: keep this file pure ASCII. cmd.exe parses .bat using the
REM  console OEM code page; UTF-8 non-ASCII text here corrupts the parse.
REM ============================================================
chcp 65001 >nul

if not exist "E:\ovhome" mkdir "E:\ovhome"
if not exist "E:\ovtmp"  mkdir "E:\ovtmp"
if not exist "E:\ovwarp" mkdir "E:\ovwarp"
set "PYTHONIOENCODING=utf-8"
set "LOCALAPPDATA=E:\ovhome"
set "TEMP=E:\ovtmp"
set "TMP=E:\ovtmp"
set "WARP_CACHE_PATH=E:\ovwarp"

if not exist "%~dp0results" mkdir "%~dp0results"

echo.
echo Opening a viewport and running the AWARE condition.
echo The planner knows the hazard is there - watch the arm steer around it.
echo Isaac takes 1-2 minutes to start. Please wait for the window.
echo.
call "E:\Isaac\isaac\python.bat" "%~dp0scripts\run_episode.py" --condition aware --out "%~dp0results\watch_aware" --gui
if errorlevel 1 goto :failed

echo.
echo Done. Wrote results\watch_aware.csv / .json
pause
exit /b 0

:failed
echo.
echo Run failed - see the error output above.
pause
exit /b 1
