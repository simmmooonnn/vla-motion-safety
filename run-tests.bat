@echo off
REM Run pure math/logic unit tests (no Isaac startup, seconds)
if not exist "E:\ovhome" mkdir "E:\ovhome"
if not exist "E:\ovtmp"  mkdir "E:\ovtmp"
if not exist "E:\ovwarp" mkdir "E:\ovwarp"
set "LOCALAPPDATA=E:\ovhome"
set "TEMP=E:\ovtmp"
set "TMP=E:\ovtmp"
set "WARP_CACHE_PATH=E:\ovwarp"
set "REPO=%~dp0"
set "FAILED=0"
for %%T in (test_config_envguard test_hazard test_metrics test_sampling_math test_validity_checks) do (
    if exist "%REPO%tests\%%T.py" (
        echo === %%T ===
        call "E:\Isaac\isaac\python.bat" "%REPO%tests\%%T.py"
        if errorlevel 1 set "FAILED=1"
    )
)
if "%FAILED%"=="1" (echo ALL TESTS: FAILED) else (echo ALL TESTS: PASSED)
exit /b %FAILED%
