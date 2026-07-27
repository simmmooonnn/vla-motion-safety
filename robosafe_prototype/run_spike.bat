@echo off
REM ============================================================
REM  Run the aware/blind carried-hazard clearance spike (robosuite/MuJoCo).
REM  Headless: no rendering is needed to measure clearance, so we disable GL,
REM  which also sidesteps Windows GL headaches.
REM
REM  NOTE: keep this file pure ASCII. cmd.exe parses .bat using the console OEM
REM  code page; UTF-8 non-ASCII text here corrupts the parse.
REM ============================================================
set "MUJOCO_GL=disable"
set "PY=C:\ProgramData\Miniconda3\envs\robosafe\python.exe"

cd /d "%~dp0"

echo.
echo === metrics self-test ===
call "%PY%" metrics.py
if errorlevel 1 goto :failed

echo.
echo === aware vs blind spike (writes results\) ===
call "%PY%" run_spike.py
if errorlevel 1 goto :failed

echo.
echo Done. See results\aware.csv / blind.csv and the comparison above.
pause
exit /b 0

:failed
echo.
echo Run failed - see the error output above.
pause
exit /b 1
