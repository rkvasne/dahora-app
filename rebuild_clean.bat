@echo off
echo ============================================
echo LIMPEZA COMPLETA E REBUILD
echo ============================================
echo.

echo [1/5] Fechando processos dahora_app...
taskkill /F /IM dahora_app*.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/5] Removendo cache do PyInstaller...
if exist build rmdir /S /Q build
if exist dist rmdir /S /Q dist
if exist __pycache__ rmdir /S /Q __pycache__
for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /S /Q "%%d"
if exist dahora_app.spec del /F /Q dahora_app.spec
echo Cache removido!

echo [3/5] Removendo arquivos .pyc...
del /S /Q *.pyc 2>nul
echo Arquivos .pyc removidos!

echo [4/5] Compilando versao limpa...
py build.py

echo [5/5] Verificando build...
if exist "dist\dahora_app_v0.1.0.exe" (
    echo.
    echo ============================================
    echo BUILD CONCLUIDO COM SUCESSO!
    echo ============================================
    echo.
    echo Executavel: dist\dahora_app_v0.1.0.exe
    echo Tamanho: 
    dir "dist\dahora_app_v0.1.0.exe" | find "dahora_app"
    echo.
    echo Execute: dist\dahora_app_v0.1.0.exe
    echo.
) else (
    echo.
    echo ============================================
    echo ERRO NO BUILD!
    echo ============================================
    echo Verifique os logs acima.
)

pause
