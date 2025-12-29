# 📅 Dahora App - Cola Timestamps Automaticamente

> **Aplicativo Windows revolucionário: cole timestamps formatados DIRETAMENTE com atalhos personalizáveis**

[![Version](https://img.shields.io/badge/version-0.2.2-blue.svg)](https://github.com/rkvasne/dahora-app)
# 📅 Dahora App

<div align="center">

![Dahora App Logo](assets/dahora_icon.png)

**O gerenciador de timestamps definitivo para Windows.**  
*Cole datas e horas formatadas instantaneamente com atalhos personalizáveis.*

[![Version](https://img.shields.io/badge/version-0.2.2-blue.svg?style=for-the-badge)](https://github.com/rkvasne/dahora-app/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg?style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg?style=for-the-badge)](tests/)

[Features](#-funcionalidades) • [Instalação](#-instalação) • [Como Usar](#-como-usar) • [Configuração](#-configuração) • [Desenvolvimento](#-desenvolvimento)

</div>

---

## 🚀 Por que Dahora App?

Cansado de digitar datas manualmente? O **Dahora App** é um utilitário de sistema leve e poderoso que revoluciona como você lida com timestamps. Ele roda silenciosamente na bandeja do sistema e permite que você cole a data e hora atual formatada em qualquer lugar, com um único atalho.

**Novo na v0.2.2:** Uma interface renovada e limpa, focada em usabilidade e rapidez para suas configurações.

## ✨ Funcionalidades

### ⚡ Produtividade Instantânea
- **Colagem Automática:** Pressione `Ctrl+Shift+Q` e o timestamp aparece magicamente onde seu cursor estiver.
- **Preservação de Clipboard:** O app salva o que você tinha copiado, cola o timestamp e restaura seu clipboard original. Transparente e fluido.
- **Atalhos Ilimitados:** Crie atalhos personalizados (ex: `Ctrl+Shift+1`) com prefixos próprios (ex: `[trabalho-29.11.2025]`).

### 🎨 Interface Moderna e Limpa
- **Foco no Conteúdo:** Design minimalista que não distrai.
- **Dark Mode:** Cores profundas e contrastes refinados para conforto visual.
- **Visual Organizado:** Cards e painéis sem bordas excessivas.

### 📋 Histórico Inteligente
- **Backup de Texto:** Mantém um histórico dos últimos textos copiados (configurável).
- **Busca Rápida:** Pressione `Ctrl+Shift+F` para pesquisar e recuperar qualquer texto do histórico instantaneamente.
- **Privacidade:** Timestamps gerados não poluem seu histórico.

### ⚙️ Controle Total
- **Formatos Flexíveis:** Personalize a data/hora (`%d/%m/%Y`, `%Y-%m-%d`, etc.).
- **Delimitadores:** Escolha entre `[]`, `()`, `{}`, ou crie o seu (`<< >>`).
- **Regras de Uso:** Defina limites de histórico, intervalos de monitoramento e notificações.

---

## 📥 Instalação

### Opção 1: Executável (Recomendado)
Não requer Python instalado. Basta baixar e rodar.

1. Vá para a página de [Releases](https://github.com/rkvasne/dahora-app/releases).
2. Baixe o arquivo `DahoraApp_v0.2.2.exe`.
3. Execute o arquivo. O ícone aparecerá na bandeja do sistema (próximo ao relógio).

### Opção 2: Rodar do Código Fonte

```bash
# 1. Clone o repositório
git clone https://github.com/rkvasne/dahora-app.git
cd dahora-app

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
python main.py
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

Toda a documentação técnica e de negócio está organizada na pasta `docs/`:

- **[📜 Histórico de Desenvolvimento](docs/DEVELOPMENT_HISTORY.md):** Detalhes profundos sobre cada fase de desenvolvimento, migrações e decisões técnicas.
- **[✅ Roadmap & Melhorias](docs/IMPROVEMENTS.md):** Checklist de tarefas, melhorias planejadas e status do projeto.
- **[💰 Análise de Precificação](docs/PRICING.md):** Estudo de mercado, estratégias de monetização e análise de valor.
- **[📝 Changelog](CHANGELOG.md):** Registro oficial de mudanças por versão.

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
    ├── IMPROVEMENTS.md          # Roadmap
    └── PRICING.md               # Business
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

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
