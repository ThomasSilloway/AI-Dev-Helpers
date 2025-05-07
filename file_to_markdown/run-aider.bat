@echo off
REM Batch file to run Aider with provided file and prompt

REM Check if arguments are provided
IF "%~1"=="" (
    echo Error: Intermediate file path not provided.
    exit /b 1
)
IF "%~2"=="" (
    echo Error: Aider prompt not provided.
    exit /b 1
)

SET INTERMEDIATE_FILE=%1
SET AIDER_PROMPT=%2

echo Running Aider on: %INTERMEDIATE_FILE%
echo With prompt: %AIDER_PROMPT%

REM Ensure Aider is in your PATH or provide the full path to aider.exe
aider --yes %INTERMEDIATE_FILE% --message %AIDER_PROMPT% --model gemini/gemini-2.0-flash-lite

IF ERRORLEVEL 1 (
    echo Aider command failed.
    exit /b %ERRORLEVEL%
)

echo Aider command completed successfully.
exit /b 0