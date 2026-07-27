@echo off
REM ============================================================
REM  Smoke test: 20 steps, headless. Verifies the pipeline runs
REM  end to end (scene builds, arm moves, CSV/JSON written).
REM  Takes a couple of minutes, mostly Isaac startup.
REM
REM  NOTE: keep this file pure ASCII. cmd.exe parses .bat using the
REM  console OEM code page, so UTF-8 Chinese text here corrupts the
REM  parse and the script fails on launch. Chinese docs live in README.md.
REM ============================================================
if not exist "E:\ovhome" mkdir "E:\ovhome"
if not exist "E:\ovtmp"  mkdir "E:\ovtmp"
if not exist "E:\ovwarp" mkdir "E:\ovwarp"
set "LOCALAPPDATA=E:\ovhome"
set "TEMP=E:\ovtmp"
set "TMP=E:\ovtmp"
set "WARP_CACHE_PATH=E:\ovwarp"

echo.
echo Running 20-step smoke test (aware condition, headless)...
echo Isaac takes 1-2 minutes to start. No output until it finishes.
echo.
call "E:\Isaac\isaac\python.bat" "%~dp0scripts\run_episode.py" --condition aware --out "%~dp0results\smoke" --steps 20
if errorlevel 1 goto :failed

echo.
echo Smoke test passed. Wrote results\smoke.csv and results\smoke.json
pause
exit /b 0

:failed
echo.
echo Smoke test failed - see the error output above.
pause
exit /b 1
