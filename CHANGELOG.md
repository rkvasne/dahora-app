# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.8] - 2025-11-04

### Added
- Implementa rotação automática de logs com `RotatingFileHandler` (limite de 5MB, mantém 3 backups)
- Adiciona validação e sanitização de configurações do usuário
- Implementa aviso de privacidade na primeira execução do aplicativo
- Cria marcador `.privacy_accepted` para evitar repetição do aviso
- Adiciona nova seção "Privacidade e Segurança" na documentação (README.md)
- Adiciona arquivo `CHECKLIST_MELHORIAS.md` com 134 tarefas de melhoria organizadas por prioridade

### Fixed
- **CRÍTICO:** Corrige path hardcoded em `build.py` que impedia build em outras máquinas
  - Substitui `E:\Dahora\dahora-app\icon.ico` por caminho relativo usando `os.path.dirname(__file__)`
  - Build agora é portável e funciona em qualquer máquina/diretório
- Adiciona tratamento robusto para arquivos `settings.json` corrompidos (JSONDecodeError)
- Implementa sanitização de caracteres de controle ASCII em configurações
- Adiciona limite de 100 caracteres para prefixo com truncamento automático

### Changed
- Renomeia arquivo de log de `qopas.log` para `dahora.log` (mais consistente com nome do app)
- Melhora documentação sobre armazenamento de dados no README
- Logs agora incluem mensagem informativa sobre sistema de rotação no startup
- Settings são automaticamente validados antes de serem aplicados

### Security
- Implementa validação de entrada para prevenir caracteres perigosos em configurações
- Adiciona aviso transparente sobre dados armazenados localmente
- Documenta práticas de privacidade (zero telemetria, dados 100% locais)

### Technical
- Adiciona import `from logging.handlers import RotatingFileHandler`
- Cria função `validate_settings()` para sanitização de configurações
- Cria função `show_privacy_notice()` para primeira execução
- Atualiza `load_settings()` com validação integrada
- Build testado e funcionando: `dahora_app_v0.0.7.exe` (31.3 MB)

### Documentation
- Expande seção "Armazenamento de dados" com detalhes sobre todos os arquivos
- Adiciona informações sobre rotação automática de logs
- Documenta política de privacidade e segurança
- Cria roadmap detalhado de melhorias futuras

## [0.0.7-3] - 2025-11-04

### Purpose
- Release de teste para validar YAML e fix do passo de hash

### Fixed
- Indentação corrigida do passo "Compute SHA-256" no workflow para permanecer dentro de `steps`
- Geração correta do nome do arquivo `.sha256` usando variável simples (`$basename`)

### Technical
- Workflow acionado por tags `v*` com build em Windows e criação de release
- Upload de `.exe` e `.sha256.txt` e extração de notas do `CHANGELOG.md`
- Usa `softprops/action-gh-release@v1`

## [0.0.7-2] - 2025-11-04

### Purpose
- Release de teste para revalidar o workflow após correção no passo de hash

### Fixed
- Correção no PowerShell ao gerar o nome do arquivo `.sha256` (remoção de subexpressão `$(...)`); agora o arquivo é criado como `<basename>.sha256.txt`

### Technical
- Ajuste no passo "Compute SHA-256" do workflow `001_release.yml` usando variáveis simples (`$basename`) para montar o nome do arquivo
- A execução do workflow em tags `v*` deve anexar `.exe` e `.sha256.txt` corretamente ao release

## [0.0.7-1] - 2025-11-04

### Purpose
- Release de teste para validar o workflow de build e release por tag (GitHub Actions)

### Added
- Workflow `.github/workflows/001_release.yml` (Windows runner)
- Automação de build com `python build.py` e upload de assets (.exe e .sha256)
- Extração automática de notas do `CHANGELOG.md` para compor o corpo do release

### Technical
- Dispara em `push` de tags `v*` (ex.: `v0.0.7-1`)
- Calcula SHA-256 no runner e anexa ao release
- Usa `softprops/action-gh-release@v1` para criar o release e enviar arquivos

## [0.0.7] - 2025-11-04

### Changed
- Notificação rápida via Tkinter ajustada para ~1.5s e visual próximo ao Windows
- Clique esquerdo no ícone aciona a mesma notificação curta do atalho
- README atualizado (versões, comportamento das notificações e clique esquerdo)
- `build.py` atualizado para gerar `dahora_app_v0.0.7.exe`

### Added
- Exceção no `.gitignore` para versionar `001_pyinstaller.spec`

### Removed
- Arquivo obsoleto `qopas_app_v0.0.5.spec` (limpeza)

### Technical
- `001_pyinstaller.spec` canônico incluído no repositório

## [0.0.6] - 2025-11-03

### Added
- Janela “Definir Prefixo” atualizada com visual próximo ao Windows 11 (ttk, tema `vista`)
- Atalho interno `Ctrl+Shift+R` para “Recarregar Itens” no menu da bandeja
- Item do menu renomeado para “Recarregar Itens” e posicionado acima do histórico

### Changed
- Documentação revisada e unificada (README e CHANGELOG)
- Correção de referências antigas para `dahora_app.py`
- README atualizado com executável correto `dahora_app_v0.0.6.exe`
- Ordem dos botões na janela de prefixo ajustada para “Cancelar | Salvar”

### Removed
- Documentos redundantes/obsoletos: `CLAUDE.md` e `SUGESTOES_NOMES.md`

### Technical
- `build.py` atualizado para gerar `dahora_app_v0.0.6.exe`
- Mantida estratégia segura de atualização de menu via ação dedicada

## [0.0.4] - 2025-11-02

### Added
- **Atualização de ícone personalizado**: Novo arquivo icon.ico incorporado no executável
- **Versão 0.0.4**: Executável atualizado com novo ícone do sistema bandeja

### Changed
- **Atualização de build**: PyInstaller configurado para usar o novo arquivo icon.ico (10,052 bytes)
- **Versão incrementada**: Atualizada de v0.0.3 para v0.0.4 para refletir nova versão do ícone

---

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