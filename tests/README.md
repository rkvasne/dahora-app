# 🧪 TESTES AUTOMATIZADOS - DAHORA APP

Este diretório contém a suíte de testes do Dahora App.

> Navegação: [README do projeto](../README.md) • [Documentação](../docs/README.md)

## 📊 Status Atual

```
✅ Suíte de testes ativa
✅ Todos os testes passando
```

## 🧪 Executar Testes

### Executar todos os testes:
```bash
py -m pytest tests/
```

### Executar com cobertura:
```bash
py -m pytest tests/ --cov=. --cov-report=html
```

Obs.: a cobertura pode variar conforme o ambiente e dependências.

### Executar testes específicos:
```bash
# Apenas testes de formatação de data/hora
py -m pytest tests/test_datetime_formatter.py

# Apenas testes de settings
py -m pytest tests/test_settings.py

# Teste específico
py -m pytest tests/test_settings.py::test_validate_settings_basic
```

### Executar em modo verbose:
```bash
py -m pytest tests/ -v
```

### Ver apenas testes que falharam:
```bash
py -m pytest tests/ -x  # Para no primeiro erro
py -m pytest tests/ --lf  # Roda apenas os últimos que falharam
```

## 📁 Estrutura de Arquivos

```
tests/
├── __init__.py                      # Marca como pacote Python
├── conftest.py                      # Fixtures compartilhadas
├── test_datetime_formatter.py       # Testes de formatação de data/hora
├── test_settings.py                 # Testes de validação de settings
└── README.md                        # Este arquivo
```

## 🔧 Fixtures Disponíveis

### `temp_data_dir`
Cria um diretório temporário para testes que é automaticamente limpo após o teste.

**Uso:**
```python
def test_algo(temp_data_dir):
    filepath = os.path.join(temp_data_dir, 'test.txt')
    # ... teste ...
```

### `sample_settings`
Retorna configurações de exemplo para testes.

**Uso:**
```python
def test_settings(sample_settings):
    assert sample_settings["prefix"] == "TEST"
```

### `sample_clipboard_history`
Retorna histórico de clipboard de exemplo.

### `create_test_json_file`
Factory fixture para criar arquivos JSON de teste.

**Uso:**
```python
def test_json(create_test_json_file):
    filepath = create_test_json_file("data.json", {"key": "value"})
    # ... teste ...
```

### `create_corrupted_json_file`
Factory fixture para criar arquivos JSON corrompidos (útil para testar tratamento de erros).

## 📋 Categorias de Testes

### 🕐 Testes de Formatação de Data/Hora
- ✅ Estrutura do formato
- ✅ Formato com prefixo
- ✅ Componentes individuais
- ✅ Validação de valores
- ✅ Consistência temporal

### ⚙️ Testes de Settings
- ✅ Validação básica
- ✅ Truncamento de prefixo longo (>100 chars)
- ✅ Remoção de caracteres de controle ASCII
- ✅ Prefixo vazio
- ✅ Prefixo ausente
- ✅ Estrutura JSON
- ✅ JSON corrompido
- ✅ Caracteres especiais
- ✅ Unicode
- ✅ Escrita atômica

## 📈 Cobertura de Código

Para gerar relatório HTML de cobertura:

```bash
py -m pytest tests/ --cov=. --cov-report=html
start htmlcov/index.html  # Windows
```

Meta: **>90% de cobertura**

## 🎯 Próximos Testes a Adicionar

- [ ] Testes de histórico de clipboard
- [ ] Testes de contador
- [ ] Testes de notificações do Windows (toasts)
- [ ] Testes de menu do system tray
- [ ] Testes de hotkeys (se possível)
- [ ] Testes de single instance (mutex)
- [ ] Testes de rotação de logs
- [ ] Testes de privacidade (primeira execução)

## 📝 Convenções

- **Nomenclatura:** `test_<funcionalidade>_<cenario>.py`
- **Organização:** Um arquivo de teste por módulo/funcionalidade
- **Docstrings:** Todos os testes devem ter descrição clara
- **Fixtures:** Usar fixtures do conftest.py quando possível
- **Mocks:** Usar `pytest-mock` para dependências externas

## 🔍 Debug de Testes

Para debug detalhado:

```bash
# Mostrar prints durante os testes
py -m pytest tests/ -s

# Mostrar variáveis locais em falhas
py -m pytest tests/ -l

# Debug com pdb (Python debugger)
py -m pytest tests/ --pdb
```

## ✅ Checklist para Novos Testes

Ao adicionar novos testes:

- [ ] Teste cobre caso de sucesso
- [ ] Teste cobre casos de erro
- [ ] Teste cobre edge cases
- [ ] Teste tem docstring clara
- [ ] Teste é independente (não depende de outros)
- [ ] Teste é rápido (<1s quando possível)
- [ ] Teste usa fixtures quando apropriado
- [ ] Teste está documentado neste README

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Python Testing Guide](https://realpython.com/pytest-python-testing/)
