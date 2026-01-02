@echo off
setlocal
cd /d "%~dp0\.."
echo ============================================
echo Dahora App - Preparar artefatos de release
echo ============================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\prepare_release_artifacts.ps1" %*
if %errorlevel% neq 0 (
  echo.
  echo ERRO: Falha ao preparar release.
  exit /b %errorlevel%
)
endlocal
