@echo off
echo Hello, World! This is a batch file.
IF NOT "%~1"=="" (
    echo First argument received: %1
)
IF NOT "%~2"=="" (
    echo Second argument received: %2
)
exit /b 0
