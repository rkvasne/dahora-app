@echo off
echo ========================================
echo   Dahora App - Instalacao de Dependencias
echo ========================================
echo.

echo [1/2] Instalando dependencias...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [2/2] Verificando instalacao...
python -c "import pystray, pyperclip, PIL; print('OK: Todas as dependencias instaladas!')"

if %errorlevel% neq 0 (
    echo.
    echo ERRO: Dependencias nao foram instaladas corretamente!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para executar: python dahora_app.py
echo Para criar o .exe: python build.py
echo.
pause

