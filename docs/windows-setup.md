# ⚠️ IMPORTANTE: Python no Windows

> Navegação: [Documentação](README.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

## Para Agentes de IA / Contribuidores

**LEIA ISTO PRIMEIRO se estiver trabalhando neste projeto no Windows!**

---

## 🔴 Problema Comum

Agentes de IA frequentemente tentam:
```powershell
python --version          # ❌ NÃO FUNCIONA neste projeto
python -m pip install X   # ❌ NÃO FUNCIONA neste projeto
python scripts/build.py          # ❌ NÃO FUNCIONA neste projeto
```

Depois de falhas, tentam:
```powershell
py --version             # ✅ FUNCIONA
py -m pip install X      # ✅ FUNCIONA
py scripts/build.py             # ✅ FUNCIONA
```

---

## ✅ Solução: Use `py` SEMPRE

**Neste projeto, SEMPRE use `py` ao invés de `python`:**

```powershell
# ✅ CORRETO (Windows Python Launcher)
py --version
py -m pip install requests
py -m pytest
py scripts/build.py
py -m http.server 8000

# ❌ ERRADO (não funciona neste ambiente)
python --version
python -m pip install requests
python -m pytest
python scripts/build.py
python -m http.server 8000
```

---

## 🤔 Por que?

1. **Windows Python Launcher (`py`)** é confiável e portável
2. **`python` command** não está configurado no PATH deste projeto
3. **venv ativado** pode causar conflitos com `python`
4. **`py` sempre funciona** (é oficial do Windows desde Python 3.3+)

---

## 🎯 Regra Simples

```
Windows + Este Projeto = USE `py` SEMPRE
```

---

## 📋 Conversão Rápida

Se vir um comando com `python`, substitua por `py`:

| ❌ Errado | ✅ Correto |
|-----------|-----------|
| `python --version` | `py --version` |
| `python -m pip install X` | `py -m pip install X` |
| `python -m pytest` | `py -m pytest` |
| `python scripts/build.py` | `py scripts/build.py` |
| `python -c "..."` | `py -c "..."` |
| `python -m http.server` | `py -m http.server` |

---

## 🤖 Para Agentes de IA

Se você é um agente (Claude, GitHub Copilot, etc) testando este código:

1. **Sempre comece com `py`** quando ver `python` em documentações
2. **Não perca tempo testando `python`** - já sabemos que não funciona
3. **Use `py` em TODOS os comandos Python**
4. **Se vir `python` em scripts, substitua por `py`**

---

## 📝 Exemplos Práticos

### ✅ Correto

```powershell
# Instalar dependências
py -m pip install -r requirements.txt

# Rodar testes
py -m pytest

# Build
py scripts/build.py

# Servidor local
py -m http.server 8000

# Com ambiente virtual
.\.venv\Scripts\Activate.ps1
py --version
```

### ❌ Errado

```powershell
# ❌ Estes não funcionam neste projeto:
python --version
python -m pip install requests
python -m pytest
python scripts/build.py
python -m http.server 8000
```

---

## 🔗 Contexto

- **SO:** Windows 10/11
- **Python Launcher:** `py` (recomendado pela Microsoft)
- **Ambiente:** Virtual environment (`.venv`)
- **Versão Python:** 3.13+

---

## ❓ Dúvidas?

Se encontrar `python` em:
- Documentação → Substitua por `py`
- Scripts → Substitua por `py`
- CI/CD → Use `py` ao invés de `python`
- Exemplos → Adapte para `py`

---

**Última atualização:** 12 de janeiro de 2026

**Atenção especial a:** Agentes de IA, contribuidores no Windows, automação de testes

