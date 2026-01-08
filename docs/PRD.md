# 📌 PRD — Dahora App (v0.2.7)

> Navegação: [Índice](INDEX.md) • [README do projeto](../README.md) • [CHANGELOG](../CHANGELOG.md)

**Documento:** Product Requirements Document (PRD)  
**Produto:** Dahora App — utilitário Windows para timestamps e clipboard  
**Versão do produto (referência):** v0.2.7  
**Status:** Final  
**Data:** 05/01/2026

---

## 1) Resumo Executivo

O Dahora App é um utilitário para Windows 10/11 que roda no system tray e permite inserir (colar) data/hora formatada diretamente na posição do cursor com hotkeys globais. O app preserva o conteúdo do clipboard, oferece histórico e busca, e é projetado com privacidade como princípio: totalmente offline, sem telemetria, dados locais.

---

## 2) Problema e Contexto

### Problema
Usuários que precisam registrar timestamps (logs, tickets, planilhas, chats, notas) perdem tempo ao digitar manualmente e frequentemente interrompem o fluxo ao alternar janelas, copiar/colar e ajustar formatação. Em muitos fluxos, “copiar timestamp” não basta: o usuário precisa inserir no cursor imediatamente.

### Oportunidade
Automatizar a inserção de timestamps com hotkeys globais, mantendo o clipboard original e oferecendo histórico/busca local, reduz fricção e aumenta produtividade em tarefas recorrentes.

---

## 3) Objetivos

### Objetivos do Produto
- Inserir timestamps rapidamente sem interromper o fluxo do usuário.
- Manter confiabilidade e previsibilidade (sem “surpresas” no clipboard).
- Garantir privacidade: operação totalmente offline e dados locais.
- Oferecer UX consistente via UI moderna (settings, busca, sobre).

### Objetivos de Negócio (indiretos)
- Facilitar adoção (download simples, sem instalador obrigatório).
- Reduzir suporte necessário (documentação clara, fluxo de release definido).

---

## 4) Público-alvo e Personas

### Persona A — Dev/QA
- Usa timestamps em logs e reportes.
- Valoriza velocidade, atalhos e consistência.

### Persona B — Suporte/Operações
- Registra atendimentos e eventos continuamente.
- Precisa de histórico e busca para recuperar informações copiadas.

### Persona C — Analista/Backoffice
- Preenche planilhas e sistemas internos.
- Precisa inserir data/hora rapidamente e manter padrão de formatação.

---

## 5) Casos de Uso (Core)

1. Inserir timestamp no cursor com uma hotkey global.
2. Preservar clipboard: inserir timestamp sem “perder” o que o usuário tinha copiado.
3. Criar e gerenciar atalhos personalizados com prefixos.
4. Manter histórico local do clipboard e buscar rapidamente.
5. Operar via system tray do Windows (menu e acesso às telas).

---

## 6) Requisitos Funcionais

### RF-01 — Execução em system tray
- O app deve iniciar e permanecer disponível no system tray do Windows.
- O usuário deve acessar ações principais pelo menu do system tray.

### RF-02 — Hotkeys globais (padrões)
- O app deve oferecer hotkeys globais para ações essenciais:
  - Inserção (colar) de timestamp.
  - Abrir busca de histórico.
  - Recarregar menu/atalhos.

### RF-03 — Inserção no cursor
- Ao acionar o atalho de inserção, o timestamp deve ser inserido no contexto atual (na posição do cursor) sem exigir colar manualmente.

### RF-04 — Preservação do clipboard
- O app deve preservar o conteúdo original do clipboard durante a inserção.
- O comportamento deve ser estável e previsível, incluindo em falhas recuperáveis.

### RF-05 — Atalhos personalizados
- O usuário deve poder criar/editar/remover atalhos adicionais.
- Cada atalho pode ter prefixo e deve inserir timestamp conforme configuração.
- Deve existir validação e prevenção de conflitos/atalhos perigosos.

### RF-06 — Configurações persistentes
- O app deve persistir configurações e dados localmente em `%APPDATA%\DahoraApp`.
- Deve existir tolerância a arquivos inválidos/corrompidos com fallback seguro.

### RF-07 — Histórico do clipboard
- O app deve manter histórico local configurável.
- Deve evitar “poluir” o histórico com timestamps gerados pelo próprio app (quando aplicável ao comportamento configurado).

### RF-08 — Busca no histórico
- O app deve oferecer UI de busca rápida no histórico com acesso por atalho global.

### RF-09 — Single instance
- O app deve impedir múltiplas instâncias simultâneas no mesmo usuário/sessão, reduzindo conflitos de hotkeys e duplicidade de monitoramento.

---

## 7) Requisitos Não-Funcionais

### RNF-01 — Privacidade
- Operação totalmente offline.
- Sem telemetria e sem envio de dados.
- Dados locais com proteção quando aplicável (ex.: criptografia no Windows para histórico).

### RNF-02 — Performance
- Inicialização rápida e baixo consumo em idle.
- Monitoramento de clipboard deve ser eficiente.

### RNF-03 — Confiabilidade e Resiliência
- Escritas atômicas onde aplicável.
- Tratamento de erros de leitura/migração (ex.: DPAPI) com fallback e preservação de dados sempre que possível.

### RNF-04 — Compatibilidade
- Compatível com Windows 10/11.

---

## 8) Regras e Comportamentos (Produto)

- O timestamp deve seguir um formato configurável (baseado em `strftime`).
- Hotkeys devem ser validadas e normalizadas.
- Se houver conflito de hotkeys, o app deve informar e impedir configuração inválida.
- O usuário deve conseguir restaurar/ajustar configurações via UI.

---

## 9) Métricas de Sucesso

- **Tempo por inserção:** queda perceptível no tempo para registrar timestamps.
- **Confiabilidade percebida:** baixa incidência de “perdi meu clipboard”.
- **Qualidade:** suíte de testes consistente e fluxo de release reproduzível.
- **Adoção:** downloads do release e feedback positivo sobre “não quebrar o fluxo”.

---

## 10) Fora de Escopo (neste PRD)

- Sincronização em nuvem / conta de usuário.
- Analytics/telemetria (explicitamente fora).
- Auto-update com instalador.
- Suporte multi-plataforma (macOS/Linux).

---

## 11) Riscos e Mitigações

- **Risco:** conflitos com hotkeys do sistema/aplicativos.  
  **Mitigação:** validação robusta, mensagens de conflito e possibilidade de customização.

- **Risco:** diferenças de comportamento de clipboard/teclado no Windows.  
  **Mitigação:** testes automatizados e rotinas de fallback.

- **Risco:** aviso de “aplicativo não reconhecido” no Windows.  
  **Mitigação:** instruções claras na landing/documentação e transparência sobre assinatura.

---

## 12) Entregáveis

- Binário `.exe` e pacote `.zip` via GitHub Releases (incluindo “latest”).
- Documentação centralizada em `docs/` (índice único).
- Suíte de testes e instruções para execução local.
