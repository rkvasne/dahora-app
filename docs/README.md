# 📚 Documentação — Dahora App

Esta pasta concentra a documentação do projeto (técnica e de produto).

## ✅ Por onde começar

- **Uso e instalação (usuário final):** veja o [README.md](../README.md) na raiz do repositório.
- **Notas de release (mudanças por versão):** [CHANGELOG.md](../CHANGELOG.md)
- **Processo de build/release (inclui Git LFS e ZIP):** [RELEASE.md](RELEASE.md)

## 🗺️ Mapa de documentos

- **Histórico de desenvolvimento:** [DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)
- **Roadmap (alto nível):** [ROADMAP.md](ROADMAP.md)
- **Precificação/mercado (estudo histórico):** [PRICING.md](PRICING.md)

## 🧭 Convenções

- **Fonte da verdade de versão:** `dahora_app/constants.py` (`APP_VERSION`).
- **Links internos:** use caminhos relativos (`docs/…`, `tests/…`).
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
