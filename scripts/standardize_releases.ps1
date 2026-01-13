Set-Alias gh "C:\Program Files\GitHub CLI\gh.exe"
$env:GH_TOKEN = (Get-Content "$HOME\.github_token" -Raw).Trim()

$releases = @{
    "v0.2.4" = "v0.2.4 - Documentacao consolidada e phase 6 completa"
    "v0.2.3" = "v0.2.3 - Consolidacao e melhorias de build"
    "v0.2.2" = "v0.2.2 - Modernizacao da interface (Windows 11 Fluent Design)"
    "v0.2.1" = "v0.2.1 - Registro automatico de atalhos"
    "v0.2.0" = "v0.2.0 - Revolucao: cola automaticamente"
    "v0.0.9" = "v0.0.9 - Melhorias de estabilidade e performance"
    "v0.0.8" = "v0.0.8 - Correcoes de bugs e otimizacoes"
    "v0.0.7-4" = "v0.0.7-4 - Ajustes finais beta"
    "v0.0.7-3" = "v0.0.7-3 - Testes beta avancados"
    "v0.0.7-2" = "v0.0.7-2 - Versao beta com melhorias"
    "v0.0.7-1" = "v0.0.7-1 - Primeira versao beta"
    "v0.0.7" = "v0.0.7 - Melhorias pre-beta"
}

Write-Host "Iniciando padronizacao..." -ForegroundColor Cyan

$updated = 0
$failed = 0

foreach ($tag in $releases.Keys) {
    $newTitle = $releases[$tag]
    Write-Host "Atualizando $tag..." -ForegroundColor Yellow
    
    gh release edit $tag --repo rkvasne/dahora-app --title $newTitle 2>&1 | Out-Null
    
    if ($?) {
        Write-Host "OK - $tag" -ForegroundColor Green
        $updated++
    } else {
        Write-Host "ERRO - $tag" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "Padronizacao concluida" -ForegroundColor Green
Write-Host "Atualizadas: $updated | Falhadas: $failed"
