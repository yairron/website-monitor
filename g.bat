@echo off
chcp 65001 >nul
echo.
echo ===================================
echo Git Upload
echo ===================================
echo.

git add .

echo.
set /p message=Enter commit message:

if "%message%"=="" (
    echo.
    echo Error: Commit message required
    pause
    exit /b 1
)

git commit -m "%message%"

if errorlevel 1 (
    echo.
    echo No changes to commit or an error occurred
    pause
    exit /b 1
)

git push

if errorlevel 1 (
    echo.
    echo Error pushing to Git
    pause
    exit /b 1
)

echo.
echo Success!
echo.
pause
