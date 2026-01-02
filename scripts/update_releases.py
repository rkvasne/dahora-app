#!/usr/bin/env python3
"""
Script para atualizar releases no GitHub via API REST
Requer: GitHub token salvo em ~/.github_token
"""

import os
import sys
import json
import requests  # type: ignore[import-untyped]
from pathlib import Path

# Configuração
OWNER = "rkvasne"
REPO = "dahora-app"
TOKEN_FILE = Path.home() / ".github_token"

# Releases para atualizar (em português)
RELEASES = {
    "v0.2.4": {
        "name": "v0.2.4 - Documentação Consolidada e Phase 6 Completa",
        "body": """## 📦 O que é novo?

### 🎯 Implementação Completa da Phase 6
- Módulo base CallbackManager (265 linhas)
- 4 implementações de handlers (495 linhas)
- Testes de integração (370 linhas)
- 84 novos testes (todos passando)

### 📚 Documentação Consolidada
- Novo docs/INDEX.md como referência central
- Rastreamento de status unificado entre todas as fases
- Formato e estrutura padronizados em toda documentação

### 🎨 Melhorias na Landing Page
- Subtítulo do hero comunicando diferencial real
- Versão de download genérica para evitar confusão
- Link para página de releases do GitHub

## 📊 Métricas
- **Testes:** 262/262 passando (100%)
- **Código:** 4500+ linhas adicionadas
- **Documentação:** 3000+ linhas adicionadas
- **Compatibilidade:** 100% mantida"""
    },
    "v0.2.3": {
        "name": "v0.2.3 - Consolidação e Melhorias de Build",
        "body": """## 📦 O que é novo?

### 🎯 Melhorias de Build e Documentação
- Índice de documentação unificada em docs/
- Guia de release com build e empacotamento
- Suporte aprimorado para Git LFS

### 🔧 Correções Importantes
- Diálogos sobre agora mostram versão atual
- Metadados de versão alinhados (0.2.3)
- Instalação prefere artefato .zip"""
    },
    "v0.2.2": {
        "name": "v0.2.2 - Modernização da Interface (Windows 11 Fluent Design)",
        "body": """## 🎨 O que é novo?

### 🎨 Interface Ultra-Moderna
- Design Fluent do Windows 11 implementado
- Tabs redesenhadas com padding uniforme
- Scrollbars modernas com estilo overlay
- Botões ultra-modernos com efeitos visuais
- Inputs aprimorados com melhor UX
- Cards com elevação e profundidade

### 🎯 Impacto Visual
- Interface 100% mais próxima do Windows 11
- Menos ruído visual com bordas removidas
- Melhor feedback em interações (hover, focus)"""
    },
    "v0.2.1": {
        "name": "v0.2.1 - Registro Automático de Atalhos",
        "body": """## 🔧 O que é novo?

### ⚡ Registro em Tempo Real
- Atalhos registrados instantaneamente ao adicionar/editar
- Sem necessidade de reiniciar o app
- Wrappers implementados para registro automático

### 🎯 Impacto
**Antes:** Adiciona atalho → Reinicia app → Funciona
**Agora:** Adiciona atalho → Funciona NA HORA! ⚡"""
    },
    "v0.2.0": {
        "name": "v0.2.0 - Revolução: Cola Automaticamente!",
        "body": """## 🔥 MUDANÇAS PRINCIPAIS

### 🚀 Funcionalidades
- Colagem Automática: Atalhos colam timestamps direto no cursor
- Atalhos Personalizáveis: Até 9 atalhos customizados
- Interface Windows 11: 5 abas profissionais
- Configuração Total: Delimitadores, formato, teclas customizáveis

### 🧠 Comportamento Inteligente
- Sistema salva clipboard, cola e restaura automaticamente
- Histórico inteligente que guarda apenas textos do usuário
- Logs otimizados (120x menos logs)"""
    }
}


def main():
    # Verificar token
    if not TOKEN_FILE.exists():
        print("❌ Token não encontrado!")
        print(f"   Salve em: {TOKEN_FILE}")
        sys.exit(1)
    
    token = TOKEN_FILE.read_text().strip()
    if not token:
        print("❌ Token está vazio!")
        sys.exit(1)
    
    # Headers para API
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Python-GitHub-Release-Updater"
    }
    
    print("\n🚀 Iniciando atualização de releases...\n")
    
    success = 0
    failed = 0
    
    for tag, data in RELEASES.items():
        api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{tag}"
        
        print(f"🔄 Atualizando {tag}...")
        
        payload = {
            "name": data["name"],
            "body": data["body"],
            "draft": False,
            "prerelease": False
        }
        
        try:
            response = requests.patch(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ {tag} atualizada com sucesso!")
                success += 1
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                failed += 1
        except Exception as e:
            print(f"❌ Erro ao atualizar {tag}: {str(e)}")
            failed += 1
        
        print()
    
    # Resultado final
    print("━" * 50)
    print(f"✅ Sucesso: {success} | ❌ Erros: {failed}")
    print("━" * 50)
    
    if failed == 0:
        print("\n🎉 Todas as releases foram atualizadas com sucesso!")
        print(f"📍 https://github.com/{OWNER}/{REPO}/releases\n")
    else:
        print(f"\n⚠️ {failed} release(s) falharam. Verifique o token.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
