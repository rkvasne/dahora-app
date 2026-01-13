# 🛠️ SCRIPTS UTILITÁRIOS - DAHORA APP

Esta pasta contém scripts auxiliares para desenvolvimento e testes.

> Navegação: [README do projeto](../README.md) • [Documentação](../docs/README.md)

---

## 📋 SCRIPTS DISPONÍVEIS

Este diretório contém scripts de apoio. O fluxo oficial de build/release está em [docs/release-process.md](../docs/release-process.md).

### 📦 Build / Release

#### **rebuild_clean.bat**
Build limpo: remove caches/artefatos e executa `py build.py`.

```powershell
scripts\rebuild_clean.bat
```

#### **prepare_release_artifacts.bat / prepare_release_artifacts.ps1**
Prepara artefatos para release e evita ZIP do repositório inteiro.

```powershell
scripts\prepare_release_artifacts.bat
# ou
powershell -ExecutionPolicy Bypass -File scripts\prepare_release_artifacts.ps1
```

#### **push_release_lfs.bat / push_release_lfs.ps1**
Ajuda a publicar artefatos grandes via Git LFS.

#### **standardize_releases.ps1**
Padroniza nomes/artefatos de releases.

#### **update_releases.py**
Auxilia atualização/organização de releases (uso interno).

### 🧩 Ícones

#### **convert_icon.py**
Conversão/manipulação de ícones (uso em build/branding).

#### **generate_icons_all.py**
Geração em lote de ícones (variações/tamanhos).

#### **clean_icons.ps1**
Limpa cache relacionado a ícones (Windows/build).

### 🔎 Debug / Diagnóstico

#### **debug_dahora.py**
Script de debug do app em ambiente de desenvolvimento.

#### **test_minimal.py**
Execução mínima para isolar problemas de import/importações/UI/system tray.

```powershell
py scripts\test_minimal.py
```

#### **test_menu.py**
Testa geração do menu do system tray.

```powershell
py scripts\test_menu.py
```

### 🧪 Experimentos / Manuais

#### **manual_shortcuts.py / manual_shortcut_editor.py**
Scripts auxiliares para testar/validar atalhos e editor.

#### **manual_ui_modernization.py**
Script auxiliar relacionado à modernização de UI (uso interno).

---

## 📁 ESTRUTURA

```
scripts/
├── README.md
├── convert_icon.py
├── debug_dahora.py
├── generate_icons_all.py
├── clean_icons.ps1
├── manual_shortcut_editor.py
├── manual_shortcuts.py
├── manual_ui_modernization.py
├── prepare_release_artifacts.bat
├── prepare_release_artifacts.ps1
├── push_release_lfs.bat
├── push_release_lfs.ps1
├── rebuild_clean.bat
├── standardize_releases.ps1
├── test_menu.py
├── test_minimal.py
└── update_releases.py
```

---

## ⚠️ IMPORTANTE

**Estes scripts são para desenvolvimento!**

- ❌ Não incluir no executável final
- ❌ Não usar em produção
- ✅ Usar apenas para testes e debugging
- ✅ Manter atualizados com versão do projeto

---

## 🔄 MANUTENÇÃO

### Versão do executável

O `rebuild_clean.bat` procura automaticamente por `dist\DahoraApp_v*.exe`.

### 📦 **prepare_release_artifacts** (recomendado para release)

Prepara os arquivos corretos para enviar ao Git LFS, evitando ZIP do repositório inteiro.

Executa:
- Move (por padrão) `DahoraApp_v*.zip/.exe` e `dahora-app-*.zip` fora de `dist/` para `.release_trash/`.
- Garante que exista `dist/DahoraApp_vX.Y.Z.zip` contendo apenas o `dist/DahoraApp_vX.Y.Z.exe`.
- Imprime os comandos `git add` recomendados.

Uso:

```bat
scripts\prepare_release_artifacts.bat
```

Ou:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\prepare_release_artifacts.ps1
```
Isso evita ter que atualizar o script a cada incremento de versão.

Para detalhes do processo de release (ZIP/LFS), veja [docs/release-process.md](../docs/release-process.md).

---

## 📝 ADICIONAR NOVOS SCRIPTS

**Padrão para novos scripts:**

1. **Nome descritivo** em inglês
2. **Comentário no topo** explicando o propósito
3. **Documentar neste README**
4. **Seguir convenções do projeto**

**Exemplo de novo script:**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para [descrição do propósito]
"""

# Código aqui...
```

---

**📌 Scripts organizados e documentados!**
