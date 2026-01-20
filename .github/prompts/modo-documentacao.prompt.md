---
description: Escrita técnica, manutenção de documentação, changelogs e guias de usuário
---

# 📚 Modo Documentação

> **Princípio:** Documentação é código. Deve ser mantida, versionada e revisada.
> **Referências:** [Google Tech Writing](https://developers.google.com/tech-writing), [Diátaxis](https://diataxis.fr)

Este modo foca na clareza, estrutura e manutenção da base de conhecimento do projeto.

---

## ⚠️ REGRAS DE OURO

### ❌ NUNCA
- ❌ **"Clique aqui"** → use links descritivos ("Consulte o Guia de Instalação")
- ❌ **Parede de texto** → use listas, negrito e quebras de linha
- ❌ **Documentar o óbvio** → não explique `print("oi")`, explique o *porquê*
- ❌ **Docs desatualizados** → se mudou o código, mudou o doc (no mesmo PR)
- ❌ **Assumir conhecimento prévio** → linke para conceitos base se necessário

### ✅ SEMPRE
- ✅ **Defina a audiência** → é para dev (técnico) ou usuário (funcional)?
- ✅ **Use imperativo** → "Faça isso", "Instale aquilo" (mais direto)
- ✅ **Exemplos copiáveis** → code blocks com botão de copy
- ✅ **Fonte Única da Verdade** → evite duplicar, linke para o original
- ✅ **Estrutura Visual** → Emojis, Callouts (Note/Warning) ajudam a leitura

---

## 📝 1. Tipos de Documentação (Diátaxis)

1.  **Tutoriais (Learning-oriented):** "Aprenda fazendo". Passo a passo prático para iniciantes.
    *   *Ex:* "Criando sua primeira API em 5 minutos".
2.  **Guias (Task-oriented):** "Como fazer X". Resolve um problema específico.
    *   *Ex:* "Como resetar a senha de admin".
3.  **Referência (Information-oriented):** "O que é X". Descrição técnica precisa.
    *   *Ex:* "Especificação da API v2", "Lista de variáveis de ambiente".
4.  **Explicação (Understanding-oriented):** "Por que X". Contexto e design.
    *   *Ex:* "Por que escolhemos PostgreSQL e não Mongo".

---

## ⚙️ 2. Fluxo de Execução (Siga nesta ordem)

1.  **Mapear:** Liste o que já existe antes de escrever.
2.  **Identificar:** Ache redundâncias e obsolescências.
3.  **Consolidar:** Junte informações dispersas no menor número de arquivos.
4.  **Padronizar:** Ajuste estilo, datas (`DD/MM/AAAA`) e estrutura.
5.  **Validar:** Teste todos os links e referências.
6.  **Confrontar:** O doc bate com o código? Se não, corrija o doc.
7.  **Finalizar:** Commit claro, sem arquivos temporários.

---

## 📄 3. Templates Comuns

### README.md (Layout Padrão "Hero Section")

O README deve seguir o padrão visual "Hero Section" (centralizado com badges) para passar profissionalismo imediato.

**Estrutura Obrigatória:**
1.  **Hero Section (Centralizada em `div align="center"`):**
    *   Título H1 (`# Nome`)
    *   Logo (SVG/PNG, 256x256px)
    *   Descrição Curta (Bold) + Subtítulo (Itálico)
    *   Badges (Estilo `for-the-badge`)
    *   Links Rápidos (Docs, Install, Contrib)
    *   **Links:** `CONTRIBUTING.md`, `LICENSE.md`, `SECURITY.md` (quando existirem).
2.  **Sobre:** O que é e por que existe.
3.  **Funcionalidades:** Lista categorizada.
4.  **Instalação/Uso:** Quick start.
5.  **Rodapé:** Créditos centralizados.

> **Template:** Use o README.md raiz do projeto como base para estruturação.

### CHANGELOG.md
Fonte única de releases. Siga [Keep a Changelog](https://keepachangelog.com):
- `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

### Pasta docs/
- Um documento canônico por assunto.
- Nomes em `lowercase-kebab-case.md`.
- Não renomeie apenas por estética.

---

## ✅ Checklist de "Padrão Profissional"
- [ ] Estrutura clara e previsível?
- [ ] Navegação fácil e lógica (Hub Central)?
- [ ] Linguagem neutra e técnica?
- [ ] Uso mínimo e consciente de emojis?
- [ ] Aparência de repositório open source maduro?

---

## 🔗 Referências
- [Google Tech Writing Courses](https://developers.google.com/tech-writing)
- [The Diátaxis Framework](https://diataxis.fr)
- [Markdown Guide](https://www.markdownguide.org)
