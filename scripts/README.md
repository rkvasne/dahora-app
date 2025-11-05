# 🛠️ SCRIPTS UTILITÁRIOS - DAHORA APP

Esta pasta contém scripts auxiliares para desenvolvimento e testes.

---

## 📋 SCRIPTS DISPONÍVEIS

### 🔨 **rebuild_clean.bat**
**Descrição:** Script de build limpo completo

**O que faz:**
1. Fecha processos `dahora_app*.exe` em execução
2. Remove cache do PyInstaller (`build/`, `dist/`, `__pycache__/`)
3. Remove arquivos `.pyc`
4. Executa `py build.py`
5. Verifica se o executável foi criado

**Como usar:**
```bash
scripts\rebuild_clean.bat
```

**Quando usar:**
- Antes de fazer release
- Quando o build está com problemas
- Para garantir build limpo sem cache

---

### 🧪 **test_menu.py**
**Descrição:** Testa geração de itens do menu

**O que faz:**
- Cria instância do `MenuBuilder`
- Define callbacks dummy
- Gera itens do menu
- Exibe lista de itens gerados

**Como usar:**
```bash
# Da raiz do projeto:
py scripts\test_menu.py

# Ou dentro da pasta scripts:
cd scripts
py test_menu.py
```

**Quando usar:**
- Para verificar estrutura do menu
- Para debugar problemas de menu
- Para validar callbacks

---

### 🔬 **test_minimal.py**
**Descrição:** Versão minimalista para isolar problemas

**O que faz:**
- Testa importações básicas
- Testa criação de ícone simples
- Testa inicialização do pystray
- Logging detalhado de cada etapa

**Como usar:**
```bash
# Da raiz do projeto:
py scripts\test_minimal.py

# Ou dentro da pasta scripts:
cd scripts
py test_minimal.py
```

**Quando usar:**
- Para isolar problemas de importação
- Para debugar inicialização
- Para testar ambiente mínimo

---

## 📁 ESTRUTURA

```
scripts/
├── README.md              (este arquivo)
├── rebuild_clean.bat      (build limpo)
├── test_menu.py           (teste de menu)
└── test_minimal.py        (teste minimalista)
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

### **Atualizar versão nos scripts:**

Quando incrementar versão do projeto, atualizar:
- `rebuild_clean.bat` → Verificação do executável

**Exemplo:**
```batch
if exist "dist\dahora_app_v0.1.1.exe" (
```

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
