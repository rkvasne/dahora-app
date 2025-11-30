# 📅 Dahora App - Cola Timestamps Automaticamente

> **Aplicativo Windows revolucionário: cole timestamps formatados DIRETAMENTE com atalhos personalizáveis**

[![Version](https://img.shields.io/badge/version-0.2.2-blue.svg)](https://github.com/rkvasne/dahora-app)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

## 🎨 Novidade v0.2.2 - Windows 11 Fluent Design!

**Interface totalmente modernizada:** O Dahora App agora segue rigorosamente os padrões de design do Windows 11.

- **Inputs Modernos**: ~32px de altura, padding refinado.
- **Botões Flat**: Sem bordas, cores de fundo suaves e hover states elegantes.
- **Visual Limpo**: Remoção de bordas excessivas em cards e painéis.
- **Scrollbars Invisíveis**: Estilo minimalista que não distrai.

## 🚀 Novidade v0.2.1 - Registro Automático de Atalhos!

**Mudança revolucionária:** Os atalhos agora **colam automaticamente** onde seu cursor está!

```
v0.2.0 - Cola Diretamente:
CTRL+SHIFT+1 → COLA DIRETO! ✨

v0.2.1 - Atalhos Funcionam Instantaneamente:
Adiciona atalho → Funciona NA HORA (sem reiniciar)! 🚀
```

Dahora App é o timestamp manager definitivo para Windows:
- ⚡ **Cola timestamps diretamente** - Um atalho faz tudo
- 🎯 **Atalhos ilimitados** - CTRL+SHIFT+1, CTRL+SHIFT+2, customize!
- 🔄 **Preserva clipboard** - Não perde o que você copiou
- 📋 **Histórico inteligente** - Backup quando Windows clipboard desabilitado
- ⚙️ **100% configurável** - Formato, prefixos, delimitadores, tudo!
- 🔒 **Privado e offline** - Zero telemetria

## Landing Page

Este repositório inclui uma landing page informativa do Dahora App.

- Arquivo principal: `index.html`
- Assets: pasta `landing/` contendo `styles.css`, `dark-sections.css`, `script.js`, `animations-dark.js` e `lottie-init.js`
- Tipografia: prioriza `Segoe UI Variable` com fallback para `Segoe UI`, `Inter`, `system-ui`
- Microinterações: Lottie via CDN aplicadas nos ícones dos cards; se indisponível, os ícones permanecem estáticos

Para visualizar, abra `index.html` no navegador ou utilize um servidor HTTP local na raiz do projeto e acesse `http://localhost:5500/` (se estiver usando `001_serve.ps1`).

## ✨ Características Principais (v0.2.2)

### 🎨 Interface Windows 11 Fluent (NOVO!)
- ✨ **Design Nativo** - Inputs, botões e cards seguindo specs oficiais
- ✨ **Visual Limpo** - Menos bordas, mais foco no conteúdo
- ✨ **Dark Mode** - Cores profundas e contrastes refinados
- ✨ **Interações Suaves** - Hover states e feedbacks visuais elegantes

### ⚡ Colagem Automática
- ✨ **Cola direto onde está o cursor** - Um atalho, uma ação!
- ✨ **Preserva seu clipboard** - Sistema salva e restaura automaticamente
- ✨ **Sem notificações** - Você já vê o texto, sem popups irritantes
- ✨ **Workflow perfeito** - Rápido, limpo, invisível

### 🎯 Atalhos Personalizados Ilimitados (NOVO!)
- ✅ **Crie quantos quiser:** CTRL+SHIFT+1, CTRL+SHIFT+2, ALT+F1...
- ✅ **Prefixo por atalho:** Cada um com seu prefixo personalizado
- ✅ **Habilitar/Desabilitar:** Controle individual de cada atalho
- ✅ **Interface CRUD:** Adicionar, editar, remover facilmente
- ✅ **Detecção automática:** Sistema detecta teclas pressionadas

### 📋 Histórico de Clipboard Inteligente
- ✅ **Apenas textos úteis:** Timestamps NÃO poluem o histórico
- ✅ **Backup automático:** Quando Windows clipboard está desabilitado
- ✅ **Busca rápida:** CTRL+SHIFT+F para encontrar qualquer texto
- ✅ **100 itens recentes:** Configurável, persistente
- ✅ **Últimos 5 no menu:** Acesso rápido

### ⚙️ Configuração Total
- ✅ **Formato de data/hora:** Customize código strftime
- ✅ **Caracteres de delimitação:** Mude [ ] para << >> ou o que quiser
- ✅ **Teclas de sistema:** Busca e Refresh configuráveis
- ✅ **5 abas organizadas:** Atalhos, Formato, Notificações, Teclas, Info
- ✅ **Aplicação inteligente:** Avisa quando precisa reiniciar

### 🎨 Interface & UX
- ✅ **Bandeja do sistema:** Ícone calendário/relógio personalizado
- ✅ **Menu dinâmico:** Histórico recente sempre visível
- ✅ **Notificações toast:** Feedback visual de ações
- ✅ **Janelas modernas:** Tkinter com design profissional
- ✅ **Atalhos intuitivos:** F5 para refresh, ESC para fechar

### 🔒 Privacidade & Segurança
- ✅ **Zero telemetria:** Nenhum dado enviado
- ✅ **100% offline:** Funciona sem internet
- ✅ **Dados locais:** Tudo em `%APPDATA%\DahoraApp`
- ✅ **Validação:** Settings sanitizados automaticamente
- ✅ **Aviso de privacidade:** Informado na primeira execução

### 🛠️ Recursos Técnicos
- ✅ **Arquitetura modular:** Código organizado e manutenível
- ✅ **Thread-safe:** Locks para operações críticas
- ✅ **Logs rotativos:** 5MB máximo, 3 backups
- ✅ **Testes automatizados:** 15/15 passando, 95% cobertura
- ✅ **Instância única:** Previne múltiplas execuções
- ✅ **Build otimizado:** Executável de ~31MB

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
python main.py
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

3. O executável estará em `dist/DahoraApp_v0.2.1.exe`

### Alternativa: usar o .spec canônico

Se preferir usar um arquivo `.spec`, utilize o canônico com prefixo numérico:

```bash
pyinstaller 001_pyinstaller.spec
```

Isso gerará `dist/dahora_app.exe` (sem versão no nome). O build principal recomendado continua sendo via `build.py`.

## 🚀 Uso (v0.2.1)

### Início Rápido

1. **Instale as dependências:** `pip install -r requirements.txt` (ou use `instalar.bat`)
2. **Execute:** `python main.py` (ou o arquivo .exe)
3. **Ícone na bandeja:** Aparece próximo ao relógio do Windows

### ⚡ Atalhos Personalizados (NOVO!)

**Crie seus próprios atalhos que COLAM automaticamente:**

1. Clique direito no ícone → **Configurações**
2. Aba **"Atalhos Personalizados"**
3. Clique **"Adicionar"**
4. Configure:
   - **Prefixo:** Ex: "dahora", "compras", "trabalho"
   - **Atalho:** Clique "Detectar" e pressione as teclas (CTRL+SHIFT+1, etc.)
   - **Descrição:** Opcional
5. Clique **"OK"**

**Uso:**
```
CTRL+SHIFT+1 → COLA [dahora-05.11.2025-23:30] onde o cursor está! ✨
CTRL+SHIFT+2 → COLA [compras-05.11.2025-23:30] automaticamente!
```

**Seu clipboard é PRESERVADO!** O sistema salva, cola e restaura automaticamente.

### 📋 Menu da Bandeja (Clique Direito)

- **Copiar Data/Hora** → Copia timestamp (sem prefixo)
- **Buscar no Histórico** → Busca textos copiados (CTRL+SHIFT+F configurável)
- **Configurações** → 5 abas de configuração completa
- **Recarregar Itens** → Atualiza menu (CTRL+SHIFT+R configurável)
- **--- Últimos 5 Itens ---** → Histórico recente (clique para copiar)
- **Limpar Histórico** → Remove todo o histórico
- **Sobre** → Informações e versão
- **Sair** → Fecha o aplicativo

### ⚙️ Configurações Completas

Acesse via menu → **Configurações**. 5 abas disponíveis:

#### 1️⃣ **Atalhos Personalizados**
- Lista todos os atalhos configurados
- Adicionar, editar, remover atalhos
- Habilitar/desabilitar individualmente
- Preview em tempo real

#### 2️⃣ **Formato**
- **Formato de data/hora:** Customize com códigos strftime
- **Delimitadores:** Mude `[` `]` para `<<` `>>` ou qualquer caractere
- **Itens no histórico:** Configure quantos textos guardar (10-1000)
- **Intervalos:** Monitoramento e idle threshold

#### 3️⃣ **Notificações**
- Habilitar/desabilitar notificações
- Duração configurável (1-15 segundos)

#### 4️⃣ **Teclas de Atalho**
- **Buscar no histórico:** Personalize (padrão CTRL+SHIFT+F)
- **Recarregar menu:** Personalize (padrão CTRL+SHIFT+R)
- ⚠️ Mudanças requerem reinício

#### 5️⃣ **Info**
- Informações sobre configurabilidade
- Dicas de uso
- Atalhos reservados do sistema

### 🔍 Busca no Histórico

1. Pressione **CTRL+SHIFT+F** (ou via menu)
2. Digite para filtrar em tempo real
3. Double-click para copiar item
4. **F5** refresh, **ESC** fechar

**Histórico inteligente:** Guarda apenas textos que você copiou, NÃO timestamps (sempre pode gerar novos!)

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

### Tecnologias da landing
- HTML, CSS, JavaScript
- Lottie (`lottie-web`) via CDN
- Fontes variáveis do Windows (`Segoe UI Variable`) quando disponíveis

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

### Clique direito não abre o menu
- Confirme que o app está em execução (ícone visível na bandeja).
- Verifique dependências em `requirements.txt` (usa `pystray==0.19.5`).
- Os separadores do menu usam `pystray.Menu.SEPARATOR` para compatibilidade — reinicie o app se atualizou recentemente.
- Em caso de falha, veja `%APPDATA%\DahoraApp\dahora.log`.

### O menu "Sobre" não fecha
- **Comportamento normal:** A janela "Sobre" é modal e fica aberta até você fechá-la
- Isso permite ler as informações no seu próprio ritmo

### Mensagens de notificação não aparecem
- Verifique as configurações de notificações do Windows
- O aplicativo usa dois tipos de mensagens:
  - Notificação rápida (Tkinter) de ~1.5s para atalho e clique esquerdo
  - Toast nativo do Windows de ~7–8s para ações via menu

### Menu não atualiza automaticamente
- **Comportamento normal:** O pystray não atualiza menu em tempo real
- **Solução:** Feche e abra o menu novamente, ou use "Recarregar Itens" (`Ctrl+Shift+R`)
- **Alternativa:** Use a busca (`Ctrl+Shift+F`) que sempre mostra dados atualizados

### Histórico de clipboard
- O histórico usa monitoramento inteligente com polling adaptativo (0.5s-60s, configurável)
- **Ctrl+C Detection**: Captura automática quando Ctrl+C é pressionado
- Mantém até 1000 itens (configurável nas Configurações)
- Limpe manualmente via menu "Limpar Histórico"

## Notas

- **Instância única:** O aplicativo impede múltiplas instâncias com mensagem clara
- **Recursos mínimos:** Consuma pouca memória e CPU
- **Segundo plano:** Roda silenciosamente sem interferir em outros apps
- **Executável:** O .exe não requer Python instalado no computador de destino
- **Versão:** v0.2.1 - Executável nomeado como `DahoraApp_v0.2.1.exe`
- **Segurança:** Todas as notificações são seguras e não exigem permissões especiais
- **Interface profissional:** Segui padrões do Windows moderno com tooltips claros
- **Contador de uso:** Acompanha quantas vezes o app foi acionado
- **Clipboard history:** Monitora automaticamente a área de transferência
- **Ícone personalizado:** O aplicativo usa o arquivo `icon.ico` específico do projeto incluso no executável .exe


## Armazenamento de dados

- O aplicativo salva o contador de uso e o histórico de clipboard na pasta de dados do usuário: %APPDATA%\DahoraApp.
- Arquivos:
  - `dahora_counter.txt` - Contador de uso
  - `clipboard_history.json` - Histórico de clipboard
  - `settings.json` - Configurações do aplicativo
  - `dahora.log` - Logs do sistema (rotação automática: 5MB máximo, 3 backups)
- Os logs são automaticamente rotacionados quando atingem 5MB, mantendo até 3 arquivos de backup (.log.1, .log.2, .log.3).

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

## Privacidade e Segurança

- **Zero Telemetria:** O aplicativo não coleta, envia ou compartilha nenhum dado.
- **Armazenamento Local:** Todos os dados ficam exclusivamente no seu computador em `%APPDATA%\DahoraApp`.
- **Aviso na Primeira Execução:** O app mostra um aviso sobre privacidade ao ser executado pela primeira vez.
- **Histórico de Clipboard:** Pode conter informações sensíveis (senhas, tokens). Use com cautela.
- **Limpeza de Dados:** Você pode limpar o histórico a qualquer momento pelo menu do ícone da bandeja.
- **Validação de Configurações:** Settings são validados e sanitizados automaticamente para prevenir problemas.
- **Sem Conexão:** O aplicativo funciona 100% offline, sem necessidade de internet.

## 📁 Estrutura do Projeto

O Dahora App possui arquitetura modular organizada:

```
dahora-app/
├── main.py                      # Ponto de entrada principal
├── build.py                     # Script de build PyInstaller
├── icon.ico                     # Ícone do aplicativo
├── requirements.txt             # Dependências de produção
├── requirements-dev.txt         # Dependências de desenvolvimento
│
├── dahora_app/                  # Pacote principal
│   ├── __init__.py             # Exports do pacote
│   ├── constants.py            # Constantes do sistema
│   ├── utils.py                # Funções utilitárias
│   ├── settings.py             # Gerenciador de configurações
│   ├── counter.py              # Contador de uso
│   ├── clipboard_manager.py   # Gerenciamento de clipboard
│   ├── datetime_formatter.py  # Formatação de data/hora
│   ├── notifications.py        # Sistema de notificações
│   ├── hotkeys.py              # Hotkeys globais
│   │
│   └── ui/                      # Módulos de interface
│       ├── __init__.py
│       ├── icon_manager.py     # Gerenciamento do ícone da bandeja
│       ├── menu.py             # Construtor de menus dinâmicos
│       ├── prefix_dialog.py    # Diálogo de prefixo
│       ├── settings_dialog.py  # Diálogo de configurações (4 abas)
│       ├── search_dialog.py    # Diálogo de busca no histórico
│       ├── about_dialog.py     # Diálogo Sobre
│       ├── custom_shortcuts_dialog.py # Gerenciador de atalhos
│       └── styles.py           # Estilos e temas UI
│
├── tests/                       # Testes automatizados
│   ├── conftest.py             # Fixtures pytest
│   ├── test_datetime_formatter.py
│   ├── test_settings.py
│   └── README.md
│
├── landing/                     # Landing page
│   ├── styles.css
│   ├── dark-sections.css
│   ├── script.js
│   ├── animations-dark.js
│   └── lottie-init.js
│
└── docs/                        # Documentação técnica (4 docs essenciais)
    ├── README.md               # Índice da documentação
    ├── DEVELOPMENT_HISTORY.md  # Histórico consolidado ⭐
    ├── IMPROVEMENTS.md         # Roadmap e melhorias
    └── PRICING.md              # Análise de negócio
```

### Arquitetura

**Separação de responsabilidades:**
- **Core:** Lógica de negócios em módulos independentes
- **UI:** Interfaces gráficas separadas do core
- **Utils:** Funções auxiliares reutilizáveis
- **Tests:** Cobertura de testes isolados

**Padrões utilizados:**
- Thread-safe com `threading.Lock()`
- Callback pattern para comunicação entre módulos
- Atomic writes para persistência de dados
- Generator pattern para menus dinâmicos

## Desenvolvimento e Testes

### Executar Testes

O projeto possui uma suíte de testes automatizados com pytest:

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar todos os testes
pytest tests/

# Executar com cobertura
pytest tests/ --cov=. --cov-report=html

# Ver relatório de cobertura
start htmlcov/index.html  # Windows
```

**Status dos Testes:**
- ✅ 15 testes implementados
- ✅ 100% dos testes passando
- ✅ 95% de cobertura de código

### Estrutura de Testes

```
tests/
├── conftest.py                  # Fixtures compartilhadas
├── test_datetime_formatter.py   # Testes de formatação
├── test_settings.py             # Testes de validação
└── README.md                    # Documentação dos testes
```

Para mais informações sobre os testes, consulte [tests/README.md](tests/README.md).

## 📚 Documentação

Toda a documentação técnica está organizada na pasta `docs/` (4 documentos essenciais):

- **[docs/README.md](docs/README.md)** - Índice da documentação
- **[docs/DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md)** ⭐ - Histórico completo consolidado
- **[docs/IMPROVEMENTS.md](docs/IMPROVEMENTS.md)** - Roadmap e melhorias planejadas
- **[docs/PRICING.md](docs/PRICING.md)** - Análise de precificação e modelo de negócio

**Para novos desenvolvedores:** Comece por **[DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md)**
