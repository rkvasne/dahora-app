# 🤝 Contribuindo — Dahora App

Obrigado por considerar contribuir com o Dahora App.

> Navegação: [README do projeto](README.md) • [Documentação](docs/README.md) • [Testes](tests/README.md)

---

## 1) Comece aqui

- Documentação: [docs/README.md](docs/README.md)
- Configuração Windows/Python: [docs/windows-python-setup.md](docs/windows-python-setup.md) (use `py`)

---

## 2) Configuração do ambiente (Windows)

1. Clone o repositório:

```powershell
git clone https://github.com/rkvasne/dahora-app.git
cd dahora-app
```

2. Instale dependências:

```powershell
py -m pip install -r requirements.txt
py -m pip install -r requirements-dev.txt
```

3. Execute testes:

```powershell
py -m pytest
```

---

## 3) Padrões de contribuição

- Mantenha mudanças pequenas e objetivas.
- Não altere arquivos não relacionados ao objetivo do PR.
- Atualize documentação quando necessário (e links internos).
- Evite adicionar dependências sem necessidade.

---

## 4) Pull Requests

Antes do PR:
- `py -m pytest` deve passar.
- Descreva claramente o problema e a solução.
- Referencie issues (se existirem).

---

## 5) Reportar bugs

Abra uma issue com:
- Passos para reproduzir
- Resultado esperado vs atual
- Versão do app
- Logs relevantes (sem dados sensíveis)
