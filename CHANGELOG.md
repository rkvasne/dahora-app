# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2025-11-02

### Added
- **Atualização de ícone personalizado**: Novo arquivo icon.ico incorporado no executável
- **Versão 0.0.4**: Executável atualizado com novo ícone do sistema bandeja

### Changed
- **Atualização de build**: PyInstaller configurado para usar o novo arquivo icon.ico (10,052 bytes)
- **Versão incrementada**: Atualizada de v0.0.3 para v0.0.4 para refletir nova versão do ícone

---

## [0.0.6] - 2025-11-03

### Added
- **Rebranding completo**: Alteração de nome do projeto de "Dahora App" para "Qopas App"
- **Novo nome**: Qopas (Q = letra do atalho Ctrl+Shift+Q, op = de cOPy, pas = parte de "paste")
- **Executável atualizado**: Novo executável `qopas_app_v0.0.6.exe` com nome do projeto atualizado

### Changed
- **Referências internas**: Todas as menções a "Dahora App" foram substituídas por "Qopas App"
- **Documentação completa**: README.md, CHANGELOG.md e CLAUDE.md atualizados com o novo nome
- **Build script atualizado**: build.py agora gera executáveis com prefixo "qopas_app"

### Technical
- **Arquivo principal renomeado**: `dahora_app.py` → `qopas_app.py`
- **Atualização de branding**: Interface do aplicativo, notificações e identificadores atualizados
- **Mantendo compatibilidade**: Todas as funcionalidades mantidas apenas com rebranding visual

---

## [0.0.5] - 2025-11-02

### Added
- **Monitoramento inteligente de clipboard**: Sistema adaptativo que reduz sobrecarga do sistema
- **Detecção de Ctrl+C**: Captura automaticamente quando usuário pressiona Ctrl+C
- **Polling adaptativo**: Intervalos dinâmicos de 0.5s a 10s baseados em atividade
- **Otimização de recursos**: Maior intervalo quando clipboard está ocioso (>30s)

### Changed
- **Performance clipboard monitoring**: Substituído polling constante por detecção inteligente
- **Eficiência do sistema**: Reduz consumo de CPU quando não há atividade no clipboard
- **Hotkeys expandidas**: Agora captura Ctrl+Shift+Q e Ctrl+C globalmente

### Technical
- **Intelligent polling**: 0.5s resposta rápida com atividade, até 10s quando ocioso
- **Activity detection**: Detecta mudanças reais no clipboard em vez de verificação constante
- **Ctrl+C interception**: Adiciona conteúdo ao histórico quando Ctrl+C é pressionado
- **Idle optimization**: Aumenta intervalos automaticamente quando sistema está ocioso

---

## [0.0.3] - 2025-11-02

### Added
- **Melhoria no monitoramento de clipboard**: Intervalo atualizado de 1 para 3 segundos para melhor performance
- **Funcionalidade de limpeza de histórico**: Opção "Limpar Histórico" no menu de clique direito para remover todo o histórico de clipboard
- **Histórico persistente**: Agora o histórico é salvo em `clipboard_history.json` e mantém entre reinicializações
- **Monitoramento ativo**: Clipboard é monitorado automaticamente a cada 3 segundos, detectando novas cópias
- **Interface aprimorada**: Melhor feedback visual e notificações ao limpar histórico

### Fixed
- **Corrigido bug de limpeza de histórico**: A função de limpar histórico agora funciona corretamente, removendo permanentemente todos os itens do arquivo
- **Corrigido bug de menu recursivo**: Eliminada recursão infinita ao atualizar menu após definir prefixo
- **Corrigido ícone de bandeja**: O ícone personalizado agora é carregado corretamente no executável sem erros
- **Melhorado tratamento de erros**: Logging robusto com fallbacks ao remover arquivo de histórico
- **Otimizado desempenho**: Intervalo de monitoramento reduzido para 3 segundos com melhor tratamento de exceções
- **Corrigido estado consistente**: Após limpar histórico, o aplicativo recarrega estado do arquivo para garantir consistência

---

## [0.0.2] - 2025-01-02

### Added
- **Melhoria no monitoramento de clipboard**: O histórico agora é atualizado instantaneamente sempre que o clipboard é modificado, não apenas ao iniciar o aplicativo
- **Melhoria no intervalo de monitoramento**: Reduzido de 2 para 1 segundo para detecção mais rápida de mudanças
- **Logging aprimorado**: Adicionado logs detalhados para monitoramento do clipboard em `dahora.log`
- **Inicialização aprimorada**: O aplicativo agora inicializa o estado atual do clipboard ao iniciar para evitar duplicações

### Fixed
- **Corrigido bug de histórico de clipboard**: O histórico só era atualizado ao abrir o aplicativo, não em tempo real
- **Corrigida inicialização do estado do clipboard**: Agora captura o estado atual do clipboard ao iniciar para comparação correta
- **Melhorado tratamento de erros**: Logging detalhado para depuração de problemas de clipboard
- **Otimizado desempenho**: Menor intervalo de verificação (1s) com melhor tratamento de erros

---

## [0.0.1] - 2025-01-02

### Added
- Versão inicial do Qopas App 0.0.1
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
- Executável nomeado como `qopas_app_v0.0.1.exe` com identificação de versão

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