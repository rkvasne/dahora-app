@echo off
setlocal
cd /d "%~dp0\.."
echo ============================================
echo Dahora App - Push Release via Git LFS
echo ============================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\push_release_lfs.ps1" %*
if %errorlevel% neq 0 (
  echo.
  echo ERRO: Falha no push para o LFS.
  exit /b %errorlevel%
)
endlocal
