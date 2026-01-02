#!/usr/bin/env pwsh

# Script para atualizar releases no GitHub usando a API REST
# Requer: GitHub token via variável de ambiente GH_TOKEN

param(
    [string]$TokenFile = "$HOME\.github_token"
)

# Dados das releases em português
$releases = @{
    "v0.2.4" = @{
        "tag_name" = "v0.2.4"
        "name" = "v0.2.4 - Documentação Consolidada e Phase 6 Completa"
        "body" = @"
## 📦 O que é novo?

### 🎯 Implementação Completa da Phase 6
- Módulo base CallbackManager (265 linhas)
- 4 implementações de handlers (495 linhas)
- Testes de integração (370 linhas)
- 84 novos testes (todos passando)

### 📚 Documentação Consolidada
- Novo `DOCUMENTATION_INDEX.md` como referência central
- Rastreamento de status unificado entre todas as fases
- Formato e estrutura padronizados em toda documentação

### 🎨 Melhorias na Landing Page
- Subtítulo do hero comunicando diferencial real
- Versão de download genérica para evitar confusão
- Link para página de releases do GitHub
- Design limpo e profissional

## 📊 Métricas

- **Testes:** 262/262 passando (100%)
- **Código:** 4500+ linhas adicionadas
- **Documentação:** 3000+ linhas adicionadas
- **Mudanças Quebrantáveis:** ZERO
- **Compatibilidade:** 100% mantida

## 📥 Download

Baixe o executável para Windows:
- **dahora_app_v0.2.4.zip** - Versão portável completa
- **dahora_app_v0.2.4.exe** - Executável instalável

## 🔗 Links Importantes

- [Changelog Completo](https://github.com/rkvasne/dahora-app/blob/main/CHANGELOG.md)
- [Documentação](https://github.com/rkvasne/dahora-app/tree/main/docs)
- [Relatório Final](https://github.com/rkvasne/dahora-app/blob/main/FINAL_REPORT_v0.2.4.md)
"@
    }
}

$owner = "rkvasne"
$repo = "dahora-app"
$token = $null

# Tentar ler token do arquivo
if (Test-Path $TokenFile) {
    $token = Get-Content $TokenFile -Raw
} else {
    Write-Host "❌ Token não encontrado em: $TokenFile"
    Write-Host ""
    Write-Host "Para usar este script:"
    Write-Host "1. Gere um token pessoal no GitHub: https://github.com/settings/tokens"
    Write-Host "2. Salve em: $TokenFile"
    Write-Host "3. Execute este script novamente"
    exit 1
}

# Headers para API GitHub
$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/vnd.github.v3+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

# Atualizar cada release
foreach ($tag, $releaseData in $releases.GetEnumerator()) {
    $apiUrl = "https://api.github.com/repos/$owner/$repo/releases/tags/$tag"
    
    Write-Host "🔄 Atualizando $tag..."
    
    $body = @{
        "name" = $releaseData.name
        "body" = $releaseData.body
        "draft" = $false
        "prerelease" = $false
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $apiUrl -Method PATCH -Headers $headers -Body $body -ContentType "application/json"
        Write-Host "✅ $tag atualizada com sucesso!"
    } catch {
        Write-Host "❌ Erro ao atualizar $tag: $($_.Exception.Message)"
    }
}

Write-Host ""
Write-Host "✨ Atualização concluída!"
