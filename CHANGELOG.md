# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2025-01-02

### Added
- Versão inicial do Dahora App 0.0.1
- Sistema de bandeja do Windows (system tray) com ícone de relógio personalizado
- Copia data e hora para a área de transferência no formato `[DD.MM.AAAA-HH:MM]`
- Tecla de atalho global: `Ctrl+Shift+Q` para copiar de qualquer lugar
- Notificações toast de 2 segundos com auto-dismiss
- Prevenção de múltiplas instâncias do aplicativo
- Janela "Sobre" modal que fica aberta até o usuário fechar
- Interface intuitiva com clique esquerdo (instruções) e clique direito (menu)
- Contador de uso - quantas vezes o app foi acionado
- Histórico de clipboard - mantém últimos 100 itens copiados
- Monitoramento automático de clipboard - detecta mudanças na área de transferência
- Menu com acesso rápido aos 5 itens de clipboard mais recentes
- Opção para limpar o histórico de clipboard manualmente
- Ícone personalizado incluso no executável .exe
- Script de build automatizado com PyInstaller
- Documentação completa em README.md e CLAUDE.md

### Changed
- Alterado hotkey global de `Ctrl+Shift+D` para `Ctrl+Shift+Q` para evitar conflitos
- Interface melhorada com tooltips claros e mensagens intuitivas
- Notificações otimizadas para 2 segundos de duração
- Menu organizado com submenus para histórico de clipboard

### Technical
- PyInstaller para build de executável Windows
- Python 3.8+ como dependência
- Bibliotecas: pystray, pyperclip, keyboard, Pillow, winotify, pywin32
- Arquivo .gitignore para controle de versão
- Repositório GitHub: https://github.com/rkvasne/dahora-app
- Executável nomeado como `dahora_app_v0.0.1.exe` com identificação de versão

### Fixed
- Corrigido erro de menu em `pystray` usando método `__add__` ao invés de `add`
- Melhorado tratamento de erros e exceções
- Corrigida inicialização de múltiplas instâncias
- Otimizado gerenciamento de threads e recursos

---

## [Versões Futuras]

### Planejado para 0.0.2
- [ ] Suporte para múltiplos formatos de data/hora configuráveis
- [ ] Opção para personalizar hotkey global
- [ ] Exportação de histórico de clipboard para arquivo
- [ ] Integração com cloud storage (opcional)
- [ ] Temas personalizados para o ícone

### Planejado para 0.1.0
- [ ] Interface gráfica completa para configurações
- [ ] Plugin system para extensões
- [ ] Suporte para macOS e Linux
- [ ] Autostart configuration
- [ ] Atalhos de teclado configuráveis via interface

### Planejado para 1.0.0
- [ ] Versão estável com todas as funcionalidades planejadas
- [ ] Documentação completa para desenvolvedores
- [ ] Testes automatizados unitários e de integração
- [ ] Instalador MSI para Windows
- [ ] Assinatura digital do executável