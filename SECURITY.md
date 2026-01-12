# 🔐 Política de Segurança — Dahora App

**Versão:** v0.2.11  
**Data:** 12/01/2026

---

## 1) Reporte de vulnerabilidades

Se você encontrar um problema de segurança:
- Abra uma **Issue** com o mínimo de detalhes públicos necessários; se envolver exploração/impacto alto, prefira reportar com discrição ao mantenedor.
- Inclua:
  - Passos para reproduzir
  - Impacto observado/esperado
  - Versão do app (ver `APP_VERSION`)
  - Ambiente (Windows 10/11)

Repositório: https://github.com/rkvasne/dahora-app

---

## 2) Escopo

O Dahora App é um utilitário local/offline. Ainda assim, são considerados problemas relevantes:
- Execução de código inesperada
- Vazamento de dados locais (ex.: leitura/exposição indevida do histórico)
- Falhas de permissões e persistência insegura
- Corrupção de dados (integridade) com impacto relevante

---

## 3) Versões suportadas

- A versão suportada é a mais recente publicada em Releases.
- Consulte o histórico em `CHANGELOG.md`.
