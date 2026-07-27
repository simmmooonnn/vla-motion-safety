@echo off
REM ============================================================
REM  Motion-Safety prototype: end-to-end experiment
REM  Runs the aware / blind conditions in separate processes,
REM  then analyses the two runs and writes the comparison plot.
REM  Includes the non-ASCII-username fixes (see README).
REM
REM  Usage:  run_experiment.bat         (headless, default)
REM          run_experiment.bat --gui   (open a viewport)
REM
REM  NOTE: keep this file pure ASCII. cmd.exe parses .bat using the
REM  console OEM code page, so UTF-8 Chinese text here corrupts the
REM  parse and the script fails on launch. Chinese docs live in README.md.
REM ============================================================
REM Switch the console to UTF-8 so the Chinese text that analyze.py prints
REM renders correctly. Safe to do here because this .bat is pure ASCII, so
REM changing the code page cannot corrupt the parsing of this file itself.
chcp 65001 >nul

if not exist "E:\ovhome" mkdir "E:\ovhome"
if not exist "E:\ovtmp"  mkdir "E:\ovtmp"
if not exist "E:\ovwarp" mkdir "E:\ovwarp"
set "PYTHONIOENCODING=utf-8"
set "LOCALAPPDATA=E:\ovhome"
set "TEMP=E:\ovtmp"
set "TMP=E:\ovtmp"
set "WARP_CACHE_PATH=E:\ovwarp"

set "REPO=%~dp0"
set "PY=E:\Isaac\isaac\python.bat"
set "GUIFLAG=%~1"

if not exist "%REPO%results" mkdir "%REPO%results"

echo.
echo === [1/3] condition: aware (planner knows about the hazard) ===
echo Isaac takes 1-2 minutes to start and each run is 600 steps.
echo No output appears until a run finishes. This is normal - please wait.
echo.
call "%PY%" "%REPO%scripts\run_episode.py" --condition aware --out "%REPO%results\aware" %GUIFLAG%
if errorlevel 1 goto :failed

echo.
echo === [2/3] condition: blind (planner does not know about the hazard) ===
echo.
call "%PY%" "%REPO%scripts\run_episode.py" --condition blind --out "%REPO%results\blind" %GUIFLAG%
if errorlevel 1 goto :failed

echo.
echo === [3/3] analysis and comparison plot ===
echo.
call "%PY%" "%REPO%scripts\analyze.py" "%REPO%results\aware" "%REPO%results\blind"
if errorlevel 1 goto :checks_failed

echo.
echo Experiment complete. Results are in %REPO%results\
echo   aware.csv / aware.json   blind.csv / blind.json   comparison.png
pause
exit /b 0

:checks_failed
echo.
echo The runs completed, but analysis reported a problem.
echo If you see FAIL lines above, the validity checks did not all pass -
echo read them before trusting any numbers. Otherwise it was a run error.
pause
exit /b 2

:failed
echo.
echo Experiment failed - see the error output above.
pause
exit /b 1
