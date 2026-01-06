# 📚 Documentação Técnica — Dahora App

Diretório central da documentação técnica do projeto.

> Navegação: [Índice](INDEX.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

---

## 🎯 Navegação Rápida

### 👉 **[INDEX.md](INDEX.md)** - Comece aqui!
> Índice completo de toda a documentação do projeto

### Para Usuários
- **[../README.md](../README.md)** - Instalação e uso do aplicativo
- **[../CHANGELOG.md](../CHANGELOG.md)** - Histórico de mudanças

### Apoio (doações opcionais)
- **[Apoie o projeto](../README.md#-apoie-o-projeto-opcional)** - Links de doação (Sponsors/Mercado Pago/PayPal/Pix) e QR codes

### Para Desenvolvedores
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura técnica
- **[DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)** - Histórico narrativo
- **[HACKS.md](HACKS.md)** - Workarounds documentados

### Para Manutenedores
- **[RELEASE.md](RELEASE.md)** - Processo de build e release
- **[GITHUB_CLI_GUIDE.md](GITHUB_CLI_GUIDE.md)** - GitHub CLI e autenticação

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
- **Atualizar ao mudar versão:**
  - `dahora_app/constants.py`
  - `README.md` (badge e download)
  - `CHANGELOG.md` (entrada `## [X.Y.Z]`)

### Qualidade
- Verificar links internos antes de commit
- Executar testes: `py -m pytest`
- Manter consistência de versão em toda documentação

