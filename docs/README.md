# 📚 Documentação Técnica — Dahora App

> **👉 [Vá para INDEX.md](INDEX.md)** — Índice completo de navegação para toda documentação.

---

## 📋 Convenções do Projeto

### Glossário por superfície (terminologia)

**Regra geral:** dentro de uma mesma superfície, evite misturar termos PT‑BR e termos técnicos em inglês.

- **Frontend (landing) e UI do app (usuário final):** preferir PT‑BR 100%.
  - Exemplos: “área de transferência”, “bandeja do sistema”, “atalhos”, “notificações do Windows”.
- **Documentação (Markdown) e textos para dev/power users:** preferir termos técnicos comuns em inglês.
  - Exemplos: `clipboard`, `system tray`, `hotkeys`, `toasts`.
- **Código (identificadores):** manter nomes e APIs em inglês; strings exibidas ao usuário seguem o padrão da UI.

### Versionamento
- **Fonte da verdade:** `dahora_app/constants.py` (`APP_VERSION`)
- **Sempre atualizar ao mudar versão:**
  - `dahora_app/constants.py`
  - `README.md` (badge e download)
  - `CHANGELOG.md` (entrada `## [X.Y.Z]`)
  - Arquivos `.spec` do PyInstaller

### Qualidade Antes de Commit
- ✅ Executar testes: `py -m pytest`
- ✅ Verificar links internos
- ✅ Atualizar `CHANGELOG.md`
- ✅ Versão consistente em todos os arquivos

