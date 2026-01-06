# 📅 Dahora App

<div align="center">

![Dahora App Logo](assets/dahora_icon.png)

**O gerenciador de timestamps definitivo para Windows.**  
*Cole datas e horas formatadas instantaneamente com atalhos personalizáveis.*

[![Version](https://img.shields.io/badge/version-0.2.6-blue.svg?style=for-the-badge)](https://github.com/rkvasne/dahora-app/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg?style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=for-the-badge)](https://choosealicense.com/licenses/mit/)
[![Tests](https://img.shields.io/badge/tests-automated-brightgreen.svg?style=for-the-badge)](tests/README.md)
[![Architecture](https://img.shields.io/badge/architecture-secure-brightblue.svg?style=for-the-badge)](docs/ARCHITECTURE.md)

[Features](#-funcionalidades) • [Instalação](#-instalação) • [Como Usar](#-como-usar) • [Configuração](#-configuração) • [Desenvolvimento](#-desenvolvimento)

</div>

---

##  Por que Dahora App?

Cansado de digitar datas manualmente? O **Dahora App** é um utilitário de sistema leve e poderoso que revoluciona como você lida com timestamps. Ele roda silenciosamente no system tray e permite que você cole a data e hora atual formatada em qualquer lugar, com uma única hotkey.

**Novo na v0.2.6:** Configurações avançadas expostas na UI, descrição opcional em atalhos personalizados e ajustes no monitoramento do clipboard.

> **Terminologia:** a UI/landing usam PT‑BR 100% (ex.: “área de transferência”, “bandeja do sistema”, “atalhos”).
> A documentação técnica pode usar termos comuns em inglês (ex.: `clipboard`, `system tray`, `hotkeys`). Veja [docs/README.md](docs/README.md).

## ✨ Funcionalidades

### ⚡ Produtividade Instantânea
- **Colagem Automática:** Pressione `Ctrl+Shift+Q` e o timestamp aparece onde seu cursor estiver.
- **Preservação de Clipboard:** Sistema preserva seu clipboard automaticamente. Cola timestamp e restaura o conteúdo original.
- **Atalhos Ilimitados:** Crie atalhos personalizados com prefixos próprios. Interface CRUD completa para gerenciar com eficiência.

### 🎨 Interface Moderna e Limpa
- **Design Renovado:** Interface renovada com design limpo e organizado.
- **Foco na Usabilidade:** Experiência do usuário otimizada e intuitiva.
- **Visual Profissional:** Cards e painéis com estética moderna.

### 📋 Histórico Inteligente
- **Armazenamento Seletivo:** Não salva timestamps gerados pelo próprio app no histórico.
- **Busca Rápida:** Pressione `Ctrl+Shift+F` para busca instantânea no histórico.
- **Privacidade:** Totalmente offline (sem telemetria), dados locais e histórico criptografado no Windows (DPAPI).

### ⚙️ Controle Total
- **Painel Completo:** 5 abas para controle total do aplicativo.
- **Configuração Flexível:** Configure formatos, delimitadores e teclas.
- **Execução Invisível:** Colagem instantânea sem popups desnecessários.

---

## 📥 Instalação

### Opção 1: Executável (Recomendado)
Não requer Python instalado. Basta baixar e rodar.

1. Baixe o arquivo `DahoraApp_latest.zip` (Assets do GitHub Release):
   - https://github.com/rkvasne/dahora-app/releases/latest/download/DahoraApp_latest.zip
2. (Alternativa) Vá para a página de [Releases](https://github.com/rkvasne/dahora-app/releases) e baixe o `DahoraApp_vX.Y.Z.zip`.
3. Extraia o ZIP e execute `DahoraApp_vX.Y.Z.exe`. O ícone aparecerá no system tray (próximo ao relógio).

### Opção 2: Rodar do Código Fonte

```bash
# 1. Clone o repositório
git clone https://github.com/rkvasne/dahora-app.git
cd dahora-app

# 2. Instale as dependências
py -m pip install -r requirements.txt

# 3. Execute
py main.py
```

---

## 🎮 Como Usar

### Hotkeys Globais
| Atalho | Ação |
|--------|------|
| `Ctrl+Shift+Q` | **Cola** o timestamp atual (ex: `[29.11.2025-22:45]`) |
| `Ctrl+Shift+F` | Abre a **Busca no Histórico** |
| `Ctrl+Shift+R` | Recarrega o menu do system tray |

### Menu do system tray
Clique com o botão direito no ícone do relógio na barra de tarefas:

- **Copiar Data/Hora:** Copia o timestamp para o clipboard (sem colar).
- **Buscar no Histórico:** Abre a janela de busca.
- **Configurações:** Abre o painel de controle completo.
- **Últimos Itens:** Acesso rápido aos 5 últimos textos copiados.

### Criando Atalhos Personalizados
1. Abra **Configurações** > **Atalhos Personalizados**.
2. Clique em **Adicionar**.
3. Defina um **Prefixo** (ex: `log`).
4. Clique em **Detectar** e pressione as teclas desejadas (ex: `Ctrl+L`).
5. Pronto! Agora `Ctrl+L` cola `[log-DATA-HORA]`.

---

## 🛠 Configuração

O Dahora App é altamente configurável através do menu **Configurações**:

- **Geral:** Altere o formato da data (códigos `strftime`), delimitadores e comportamento ao iniciar.
- **Histórico:** Ajuste quantos itens manter e a sensibilidade do monitoramento.
- **Notificações:** Ative/desative notificações do Windows (toasts) ou popups rápidos.
- **Teclas:** Redefina as hotkeys globais de busca e recarregamento.
- **Avançado:** Ajuste logs e otimizações internas.
  - **Tamanho máximo do log (MB)** (`log_max_bytes`): padrão 1 MB (recomendado 1–5 MB).
  - **Backups do log** (`log_backup_count`): padrão 1 (recomendado 1–2).
  - **Delay de pré-aquecimento da UI (ms)** (`ui_prewarm_delay_ms`): padrão 700 ms.
  - **Janela de cache do menu (ms)** (`tray_menu_cache_window_ms`): padrão 200 ms.

Os dados são salvos localmente em `%APPDATA%\DahoraApp`.

---

## 📚 Documentação

Toda documentação está organizada em `docs/` com índice centralizado:

### 👉 **[docs/INDEX.md](docs/INDEX.md)** - Índice Central (comece aqui!)

### Destaques:
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura técnica detalhada
- **[DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md)** - Histórico narrativo de desenvolvimento
- **[RELEASE.md](docs/RELEASE.md)** - Processo de build, release e Git LFS
- **[GITHUB_CLI_GUIDE.md](docs/GITHUB_CLI_GUIDE.md)** - GitHub CLI e autenticação
- **[HACKS.md](docs/HACKS.md)** - Soluções criativas documentadas
- **[ROADMAP.md](docs/ROADMAP.md)** - Próximos passos
- **[CHANGELOG.md](CHANGELOG.md)** - Registro oficial de mudanças

## 📂 Estrutura do Projeto

```
dahora-app/
├── main.py                      # Entry point
├── build.py                     # Script de build (PyInstaller)
├── index.html                   # Landing page (site)
├── assets/                      # Imagens e recursos
├── scripts/                     # Scripts utilitários (ícones, debug)
│   └── README.md                # Doc dos scripts
│
├── tests/                       # Testes automatizados
│   └── README.md                # Doc dos testes
│
├── dahora_app/                  # Core package
│   ├── handlers/                # Handlers de ações (callbacks)
│   ├── ui/                      # Interface (CustomTkinter/Pystray)
│   ├── clipboard_manager.py     # Monitoramento e histórico
│   ├── hotkeys.py               # Hotkeys globais
│   ├── settings.py              # Configurações e persistência
│   └── constants.py             # Constantes (APP_VERSION)
│
└── docs/                        # Documentação Centralizada
    ├── INDEX.md                 # Índice centralizado (comece aqui!)
    ├── ARCHITECTURE.md          # Arquitetura técnica
    ├── DEVELOPMENT_HISTORY.md   # Histórico narrativo
    ├── GITHUB_CLI_GUIDE.md      # GitHub CLI (autenticação, releases, workflows)
    ├── HACKS.md                 # Workarounds e decisões não-ideais
    ├── PRICING.md               # Estudo histórico de precificação
    ├── RELEASE.md               # Build/Release/ZIP/LFS
    ├── ROADMAP.md               # Próximos passos
    └── WINDOWS_PYTHON_SETUP.md  # Configuração do Python no Windows (use `py`)
```

## 🔒 Segurança & Qualidade

### Status de Implementação
- ✅ **Fase 1:** Endurecimento de segurança (66 testes)
  - Hotkey validation
  - Pydantic schemas
  - Type hints
  
- ✅ **Fase 4:** Gerenciador de instância única (21 testes)
  - Windows mutex
  - Instance protection
  
- ✅ **Fase 5:** Sincronização de threads (24 testes)
  - Race condition fixes
  - Safe shutdown coordination
  
- ✅ **Fase 6:** Consolidação da lógica de callbacks (84 testes)
  - Base `CallbackManager` (31 testes)
  - Handler implementations (35 testes)
  - Integration tests (18 testes)
  
**Total:** 266/266 testes passando (100%)

### Documentação
Comece por [docs/INDEX.md](docs/INDEX.md).

---

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md).

---

---

## ☕ Apoie o Projeto (Opcional)

Se o Dahora App te ajuda no dia a dia e você quiser apoiar o desenvolvimento, você tem várias formas de contribuir financeiramente:

### 💳 Métodos de Doação

- **GitHub Sponsors** → https://github.com/sponsors/rkvasne
- **Mercado Pago** (Brasil) → https://link.mercadopago.com.br/kvasne
- **PayPal** (Internacional) → https://www.paypal.com/donate/?hosted_button_id=JJFQZK647286S
- **Pix** (Brasil) → `fa550c5d-fdaf-4484-b52b-760071fe524d`

### 📱 QR Codes (Pix / PayPal)

Escaneie para doação rápida via **Pix** ou **PayPal**:

<div align="center">

| Pix | PayPal |
|:---:|:------:|
| ![QR Pix](landing/images/qr_pix.png) | ![QR PayPal](landing/images/qr_paypal.png) |

</div>

### 🤝 Outras Formas de Apoio

Não tem condições financeiras? Sem problema! Você também pode ajudar:
- Contribuindo com **issues, PRs e sugestões** de melhoria
- Divulgando o projeto com amigos e na comunidade
- Reportando bugs e sugestões de features

> **Nota:** O Dahora App permanece **100% open-source e gratuito**. Doações são completamente opcionais e ajudam a manter o ritmo de desenvolvimento e novas features.

---

## 🔒 Privacidade

**Resumo:** o Dahora App opera **totalmente offline** e **não coleta telemetria**.

Detalhes em [PRIVACY.md](PRIVACY.md).

---

<div align="center">

**Desenvolvido por [Raphael Kvasne](https://github.com/rkvasne)**

</div>
