# 📅 Dahora App

<div align="center">

![Dahora App Logo](assets/dahora_icon.png)

**O gerenciador de timestamps definitivo para Windows.**  
*Cole datas e horas formatadas instantaneamente com atalhos personalizáveis.*

[![Version](https://img.shields.io/badge/version-0.2.4-blue.svg?style=for-the-badge)](https://github.com/rkvasne/dahora-app/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg?style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-262%2F262-brightgreen.svg?style=for-the-badge)](tests/)
[![Architecture](https://img.shields.io/badge/architecture-secure-brightblue.svg?style=for-the-badge)](docs/ARCHITECTURE.md)

[Features](#-funcionalidades) • [Instalação](#-instalação) • [Como Usar](#-como-usar) • [Configuração](#-configuração) • [Desenvolvimento](#-desenvolvimento)

</div>

---

## � Segurança & Qualidade

### Status de Implementação
- ✅ **Phase 1:** Security Hardening (66 testes)
  - Hotkey validation
  - Pydantic schemas
  - Type hints
  
- ✅ **Phase 4:** Single Instance Manager (21 testes)
  - Windows mutex
  - Instance protection
  
- ✅ **Phase 5:** Thread Synchronization (24 testes)
  - Race condition fixes
  - Safe shutdown coordination
  
- ✅ **Phase 6:** Callback Logic Consolidation (84 testes)
  - CallbackManager base (31 testes)
  - Handler implementations (35 testes)
  - Integration tests (18 testes)
  
**Total:** 262/262 testes passando (100%)

### Documentação
Veja [docs/](docs/) para documentação completa:
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Índice centralizado (comece aqui!)
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitetura detalhada
- [HACKS.md](docs/HACKS.md) - Problemas identificados e soluções
- [DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md) - Histórico técnico
- [PHASE_6_PROGRESS.md](PHASE_6_PROGRESS.md) - Progresso da Fase 6 (completa)

---

## �🚀 Por que Dahora App?

Cansado de digitar datas manualmente? O **Dahora App** é um utilitário de sistema leve e poderoso que revoluciona como você lida com timestamps. Ele roda silenciosamente na bandeja do sistema e permite que você cole a data e hora atual formatada em qualquer lugar, com um único atalho.

**Novo na v0.2.4:** Documentação consolidada e unificada, Phase 6 completa com sistema de callbacks, **262 testes automatizados passando**, arquitetura refatorada e pronta para produção.

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
- **Armazenamento Seletivo:** Armazena apenas textos úteis, ignora timestamps.
- **Busca Rápida:** Pressione `Ctrl+Shift+F` para busca instantânea no histórico.
- **Privacidade:** Dados locais, zero telemetria.

### ⚙️ Controle Total
- **Painel Completo:** 5 abas para controle total do aplicativo.
- **Configuração Flexível:** Configure formatos, delimitadores e teclas.
- **Execução Invisível:** Colagem instantânea sem popups desnecessários.

---

## 📥 Instalação

### Opção 1: Executável (Recomendado)
Não requer Python instalado. Basta baixar e rodar.

1. Vá para a página de [Releases](https://github.com/rkvasne/dahora-app/releases).
2. Baixe o arquivo `DahoraApp_v0.2.4.zip`.
3. Extraia o ZIP e execute `DahoraApp_v0.2.4.exe`. O ícone aparecerá na bandeja do sistema (próximo ao relógio).

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

### Atalhos Globais
| Atalho | Ação |
|--------|------|
| `Ctrl+Shift+Q` | **Cola** o timestamp atual (ex: `[29.11.2025-22:45]`) |
| `Ctrl+Shift+F` | Abre a **Busca no Histórico** |
| `Ctrl+Shift+R` | Recarrega o menu da bandeja |

### Menu da Bandeja
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
- **Notificações:** Ative/desative toasts do Windows ou popups rápidos.
- **Teclas:** Redefina os atalhos globais de busca e recarregamento.

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
├── assets/                      # Imagens e recursos
├── scripts/                     # Scripts utilitários (ícones, debug)
│   └── README.md                # Doc dos scripts
│
├── tests/                       # Testes automatizados
│   └── README.md                # Doc dos testes
│
├── dahora_app/                  # Core package
│   ├── ui/                      # Interface Gráfica (Tkinter/Pystray)
│   ├── managers/                # Lógica de negócio
│   └── utils.py                 # Utilitários
│
└── docs/                        # Documentação Centralizada
    ├── DEVELOPMENT_HISTORY.md   # Histórico detalhado
    ├── README.md                # Índice da documentação
    ├── ROADMAP.md               # Roadmap
    ├── RELEASE.md               # Build/Release/ZIP/LFS
    └── PRICING.md               # Business
```

---

## 🤝 Contribuindo

Valorizamos contribuições! Sinta-se à vontade para abrir issues ou enviar pull requests.

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 🔒 Privacidade

O Dahora App foi construído com privacidade em mente:
*   **Zero Telemetria:** Nenhum dado sai do seu computador.
*   **Offline:** Funciona 100% sem internet.
*   **Dados Locais:** Histórico e configurações ficam apenas na sua máquina.

---

<div align="center">

**Feito com 💙 por [Rafael Kvasne](https://github.com/rkvasne)**

[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=flat-square)](LICENSE)

</div>
