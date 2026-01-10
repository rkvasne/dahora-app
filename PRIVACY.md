# 🔒 Política de Privacidade — Dahora App

**Resumo:** O Dahora App opera **totalmente offline** e **não coleta telemetria**.  
**Versão:** v0.2.10  
**Data:** 10/01/2026

---

## 1) O que o Dahora App coleta?

O Dahora App **não coleta** informações pessoais para envio a servidores, pois:
- Não possui backend próprio.
- Não faz chamadas de telemetria/analytics.
- Não envia dados do usuário para a internet.

---

## 2) Onde os dados ficam armazenados?

O Dahora App armazena dados **localmente** na máquina do usuário, em:

`%APPDATA%\DahoraApp`

Exemplos de dados locais que podem existir:
- Configurações (`settings.json`)
- Histórico do clipboard (`clipboard_history.json`, ou equivalente)
- Logs locais (`dahora.log`, quando habilitado)

---

## 3) Criptografia (Windows)

Quando aplicável, o Dahora App utiliza mecanismos do Windows para proteger dados locais sensíveis (ex.: DPAPI para histórico/itens protegidos). Isso significa que:
- A proteção é vinculada ao ambiente/usuário do Windows.
- Se a proteção falhar ao migrar dados antigos, o app deve usar fallback seguro (conforme comportamento atual do projeto).

---

## 4) Compartilhamento com terceiros

O Dahora App **não compartilha dados** com terceiros por padrão.

---

## 5) Internet e permissões

O Dahora App funciona sem internet. Se o usuário optar por acessar links (ex.: GitHub, Releases, site), isso ocorre no navegador, fora do app.

---

## 6) Como apagar os dados

Para remover os dados locais:
1. Feche o Dahora App.
2. Apague a pasta: `%APPDATA%\DahoraApp`

---

## 7) Contato

Para dúvidas sobre privacidade, use o canal do repositório:
- Issues: https://github.com/rkvasne/dahora-app/issues
