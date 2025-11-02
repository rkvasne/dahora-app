# Dahora App - Sistema de Bandeja do Windows

Aplicativo Windows que fica na bandeja do sistema (system tray) para copiar a data e hora atual para a área de transferência no formato `[DD.MM.AAAA-HH:MM]`.

## Características

- ✅ **Bandeja do sistema (system tray)** com ícone de calendário/relógio personalizado
- ✅ **Clique esquerdo**: Mostra instruções de uso
- ✅ **Clique direito**: Abre menu completo de opções
- ✅ **Tecla de atalho global:** `Ctrl+Shift+D` para copiar de qualquer lugar
- ✅ **Formato:** `[DD.MM.AAAA-HH:MM]` (exemplo: `[25.12.2024-14:30]`)
- ✅ **Notificações toast** de 2 segundos com auto-dismiss
- ✅ **Prevenção de múltiplas instâncias** com mensagem clara
- ✅ **Janela "Sobre" modal** que fica aberta até o usuário fechar
- ✅ **Interface intuitiva** e profissional

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

3. O executável estará em `dist/dahora_app.exe`

## Uso

1. **Primeiro, instale as dependências** (veja seção Instalação acima)
2. Execute o aplicativo: `python dahora_app.py` (ou o arquivo .exe)
3. O ícone de calendário/relógio aparecerá na bandeja do sistema (canto inferior direito, próximo ao relógio)

### Formas de usar o aplicativo:

- **Clique esquerdo no ícone** → Mostra instruções ("Menu de opções disponível")
- **Clique direito no ícone** → Abre menu completo:
  - **Copiar Data/Hora (Ctrl+Shift+D)**: Copia a data/hora atual
  - **Sobre**: Abre janela com informações do aplicativo
  - **Sair**: Fecha o aplicativo
- **Tecla de atalho:** `Ctrl+Shift+D` → Copia de qualquer aplicativo instantaneamente

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
- Verifique se `Ctrl+Shift+D` não está sendo usado por outro aplicativo

### Não consigo copiar via clique esquerdo
- **Comportamento normal:** Clique esquerdo mostra instruções, não copia
- Use clique direito para menu ou atalho `Ctrl+Shift+D` para copiar

### O menu "Sobre" não fecha
- **Comportamento normal:** A janela "Sobre" é modal e fica aberta até você fechá-la
- Isso permite ler as informações no seu próprio ritmo

### Mensagens de notificação não aparecem
- Verifique as configurações de notificações do Windows
- O aplicativo usa toast notifications que podem estar desativadas
- As mensagens duram 2 segundos e desaparecem automaticamente

## Notas

- **Instância única:** O aplicativo impede múltiplas instâncias com mensagem clara
- **Recursos mínimos:** Consuma pouca memória e CPU
- **Segundo plano:** Roda silenciosamente sem interferir em outros apps
- **Executável:** O .exe não requer Python instalado no computador de destino
- **Segurança:** Todas as notificações são seguras e não exigem permissões especiais
- **Interface profissional:** Segui padrões do Windows moderno com tooltips claros

