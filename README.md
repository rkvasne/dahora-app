# Dahora App - Sistema de Bandeja do Windows

Aplicativo Windows que fica na bandeja do sistema (system tray) para copiar a data e hora atual para a área de transferência no formato `[DD.MM.AAAA-HH:MM]`.

## Características

- ✅ **Bandeja do sistema (system tray)** com ícone de calendário/relógio personalizado
- ✅ **Clique esquerdo**: Mostra instruções de uso
- ✅ **Clique direito**: Abre menu completo de opções
- ✅ **Tecla de atalho global:** `Ctrl+Shift+Q` para copiar de qualquer lugar
- ✅ **Formato:** `[DD.MM.AAAA-HH:MM]` (exemplo: `[25.12.2024-14:30]`)
- ✅ **Notificações toast** de 2 segundos com auto-dismiss
- ✅ **Prevenção de múltiplas instâncias** com mensagem clara
- ✅ **Janela "Sobre" modal** que fica aberta até o usuário fechar
- ✅ **Interface intuitiva** e profissional
- 📊 **Contador de uso** - quantas vezes o app foi acionado
- 📋 **Histórico de clipboard** - mantém últimos 100 itens copiados com acesso rápido no menu
- 🔍 **Monitoramento automático** - detecta mudanças na área de transferência a cada 3 segundos
- 🗑️ **Limpar histórico** - opção para remover todo o histórico de clipboard manualmente
- 💾 **Histórico persistente** - salva automaticamente entre reinicializações
- 🎨 **Ícone personalizado** (icon.ico) incluso no executável .exe

## Instalação

### ⚠️ IMPORTANTE: Instale as dependências primeiro!

Antes de executar o aplicativo, você **deve** instalar as dependências. Se não instalar, receberá o erro: `ModuleNotFoundError: No module named 'pystray'`

### Opção 1: Instalação automática (Windows)

**Método mais simples:** Clique duas vezes no arquivo `instalar.bat` ou execute:
```bash
instalar.bat
```

### Opção 2: Instalação manual

1. Instale Python 3.8 ou superior
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
python dahora_app.py
```

### Opção 3: Criar executável Windows (.exe)

1. Instale PyInstaller:
```bash
pip install pyinstaller
```

2. Execute o script de build:
```bash
python build.py
```

**Importante:** O build usará automaticamente o arquivo `icon.ico` existente no projeto. Se o arquivo não existir, o script tentará criar um ícone padrão.

3. O executável estará em `dist/dahora_app_v0.0.3.exe`

## Uso

1. **Primeiro, instale as dependências** (veja seção Instalação acima)
2. Execute o aplicativo: `python dahora_app.py` (ou o arquivo .exe)
3. O ícone de calendário/relógio aparecerá na bandeja do sistema (canto inferior direito, próximo ao relógio)

### Formas de usar o aplicativo:

- **Clique esquerdo no ícone** → Mostra instruções ("Menu de opções disponível")
- **Clique direito no ícone** → Abre menu completo:
  - **Copiar Data/Hora (Ctrl+Shift+Q)**: Copia a data/hora atual
  - **--- Histórico Recente ---**: Itens do clipboard copiados recentemente (clique para copiar)
  - **Limpar Histórico**: Remove permanentemente todo o histórico de clipboard
  - **Sobre**: Abre janela com informações do aplicativo
  - **Sair**: Fecha o aplicativo
- **Tecla de atalho:** `Ctrl+Shift+Q` → Copia de qualquer aplicativo instantaneamente

## Formato de Saída

O formato gerado é sempre: `[DD.MM.AAAA-HH:MM]`

Exemplos:
- `[25.12.2024-14:30]`
- `[01.01.2025-09:15]`
- `[15.06.2024-23:45]`

## Tecnologias

- Python 3.8+
- pystray (system tray)
- pyperclip (clipboard)
- keyboard (hotkeys globais)
- Pillow (ícone personalizado)
- winotify (toast notifications)
- pywin32 (Win32 API integration)
- JSON (histórico de clipboard)
- threading (concorrência)

## Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'pystray'"
**Solução:** Execute `pip install -r requirements.txt` ou use o arquivo `instalar.bat`

### O aplicativo não aparece na bandeja
- Verifique se há mensagens de erro no console
- Certifique-se de que as dependências estão instaladas
- No Windows, o ícone pode estar oculto - clique na seta ^ na bandeja para ver todos os ícones

### Tecla de atalho não funciona
- No Windows, pode ser necessário executar como administrador para hotkeys globais
- Alguns antivírus podem bloquear hotkeys globais
- Verifique se `Ctrl+Shift+Q` não está sendo usado por outro aplicativo

### Não consigo copiar via clique esquerdo
- **Comportamento normal:** Clique esquerdo mostra instruções, não copia
- Use clique direito para menu ou atalho `Ctrl+Shift+Q` para copiar

### O menu "Sobre" não fecha
- **Comportamento normal:** A janela "Sobre" é modal e fica aberta até você fechá-la
- Isso permite ler as informações no seu próprio ritmo

### Mensagens de notificação não aparecem
- Verifique as configurações de notificações do Windows
- O aplicativo usa toast notifications que podem estar desativadas
- As mensagens duram 2 segundos e desaparecem automaticamente

### Histórico de clipboard não atualizado
- O histórico é salvo automaticamente a cada 3 segundos de monitoramento
- O histórico mantém os últimos 100 itens copiados
- Você pode limpar o histórico manualmente através do menu opção "Limpar Histórico"

## Notas

- **Instância única:** O aplicativo impede múltiplas instâncias com mensagem clara
- **Recursos mínimos:** Consuma pouca memória e CPU
- **Segundo plano:** Roda silenciosamente sem interferir em outros apps
- **Executável:** O .exe não requer Python instalado no computador de destino
- **Versão:** v0.0.3 - Executável nomeado como `dahora_app_v0.0.3.exe`
- **Segurança:** Todas as notificações são seguras e não exigem permissões especiais
- **Interface profissional:** Segui padrões do Windows moderno com tooltips claros
- **Contador de uso:** Acompanha quantas vezes o app foi acionado
- **Clipboard history:** Monitora automaticamente a área de transferência
- **Ícone personalizado:** O aplicativo usa o arquivo `icon.ico` específico do projeto incluso no executável .exe


## Armazenamento de dados

- O aplicativo salva o contador de uso e o histórico de clipboard na pasta de dados do usuário: %APPDATA%\DahoraApp.
- Arquivos: dahora_counter.txt e clipboard_history.json.

## Prefixo configurável

- É possível definir um prefixo que será incluído no texto de data/hora copiado.
- Como usar:
  - Clique com o botão direito no ícone da bandeja.
  - Selecione a opção `Definir Prefixo...` e digite o texto desejado.
  - O prefixo é salvo e passa a compor o formato de saída.
- Formato resultante:
  - Sem prefixo: `[DD.MM.AAAA-HH:MM]`
  - Com prefixo (ex.: "dahora"): `[dahora-DD.MM.AAAA-HH:MM]`
- Persistência:
  - O prefixo é salvo em `%APPDATA%\DahoraApp\settings.json`.
- Dica:
  - Para remover, defina o prefixo como vazio.
