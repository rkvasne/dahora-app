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

### Para Desenvolvedores
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura técnica
- **[DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)** - Histórico narrativo
- **[HACKS.md](HACKS.md)** - Workarounds documentados

### Para Manutenedores
- **[RELEASE.md](RELEASE.md)** - Processo de build e release
- **[GITHUB_CLI_GUIDE.md](GITHUB_CLI_GUIDE.md)** - GitHub CLI e autenticação

---

## 📋 Convenções do Projeto

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

