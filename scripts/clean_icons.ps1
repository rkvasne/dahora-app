# Script para Limpar Cache de Ícones do Windows
# Resolve problema de ícones antigos aparecendo em executáveis

Write-Host "=== Limpando Cache de Ícones do Windows ===" -ForegroundColor Cyan
Write-Host ""

# 1. Parar o Windows Explorer
Write-Host "1. Parando Windows Explorer..." -ForegroundColor Yellow
taskkill /f /im explorer.exe 2>$null
Start-Sleep -Seconds 2

# 2. Limpar cache de ícones
Write-Host "2. Removendo arquivos de cache..." -ForegroundColor Yellow

$iconsDbPath = "$env:LOCALAPPDATA\IconCache.db"
$iconsDir = "$env:LOCALAPPDATA\Microsoft\Windows\Explorer"

# Remove IconCache.db principal
if (Test-Path $iconsDbPath) {
    Remove-Item $iconsDbPath -Force -ErrorAction SilentlyContinue
    Write-Host "   ✓ IconCache.db removido" -ForegroundColor Green
}

# Remove arquivos de cache do Explorer
if (Test-Path $iconsDir) {
    Get-ChildItem -Path $iconsDir -Filter "iconcache*.db" -Force -ErrorAction SilentlyContinue | 
        ForEach-Object {
            Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
            Write-Host "   ✓ $($_.Name) removido" -ForegroundColor Green
        }
    
    Get-ChildItem -Path $iconsDir -Filter "thumbcache*.db" -Force -ErrorAction SilentlyContinue | 
        ForEach-Object {
            Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
            Write-Host "   ✓ $($_.Name) removido" -ForegroundColor Green
        }
}

# 3. Reiniciar Windows Explorer
Write-Host "3. Reiniciando Windows Explorer..." -ForegroundColor Yellow
Start-Process explorer.exe
Start-Sleep -Seconds 2

# 4. Atualizar ícones
Write-Host "4. Atualizando ícones..." -ForegroundColor Yellow
ie4uinit.exe -show 2>$null

Write-Host ""
Write-Host "=== Cache de Ícones Limpo! ===" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Cyan
Write-Host "- Aguarde 30 segundos para o cache reconstruir" -ForegroundColor White
Write-Host "- Se o ícone ainda estiver errado, reinicie o computador" -ForegroundColor White
Write-Host "- Delete o .exe antigo antes de gerar novo build" -ForegroundColor White
Write-Host ""
