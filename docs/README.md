# 📚 Documentação — Dahora App

Esta pasta concentra a documentação técnica do projeto.

## ✅ Por onde começar

- **Índice centralizado (recomendado):** veja o [DOCUMENTATION_INDEX.md](../DOCUMENTATION_INDEX.md) na raiz
- **Uso e instalação (usuário final):** veja o [README.md](../README.md) na raiz do repositório
- **Notas de release (mudanças por versão):** [CHANGELOG.md](../CHANGELOG.md)
- **Processo de build/release (inclui Git LFS e ZIP):** [RELEASE.md](RELEASE.md)

## 🗺️ Documentação Técnica

- **Arquitetura e Design:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Problemas e Soluções:** [HACKS.md](HACKS.md)
- **Histórico de Desenvolvimento:** [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)
- **Roadmap (futuro):** [ROADMAP.md](ROADMAP.md)
- **Pesquisa de Mercado:** [PRICING.md](PRICING.md)

## 🧭 Convenções

- **Fonte da verdade de versão:** `dahora_app/constants.py` (`APP_VERSION`).
- **Links internos:** use caminhos relativos (`docs/…`, `tests/…`, etc).
- **Atualização mínima obrigatória ao mudar versão:**
  - `dahora_app/constants.py`
  - `README.md` (badge + arquivo de download)
  - `CHANGELOG.md` (entrada `## [X.Y.Z]`)
  - `docs/RELEASE.md` (se o processo mudar)

## ✅ Qualidade

Antes de enviar mudanças:
- Garanta que links internos não quebraram.
- Garanta que a versão exibida é consistente nos pontos principais.
- Rode testes (`pytest`).
- Consulte [DOCUMENTATION_INDEX.md](../DOCUMENTATION_INDEX.md) para estrutura completa.

