# 🎯 Configuração de Atalhos - Dahora App

## ✨ Total Liberdade!

**NENHUM atalho é fixo!** Você configura tudo!

## 📋 Atalhos Reservados (Não Disponíveis)

Apenas atalhos básicos de clipboard:
- `Ctrl+C` (Copiar)
- `Ctrl+V` (Colar)
- `Ctrl+X` (Recortar)
- `Ctrl+A` (Selecionar Tudo)
- `Ctrl+Z` (Desfazer)

**Todos os outros estão disponíveis!**

## 🚀 Como Configurar

### **1. Abra as Configurações**
- Clique direito no ícone da bandeja
- Selecione "⚙️ Configurações"
- Vá para a aba "Prefixos"

### **2. Adicione Seus Atalhos**

**Exemplo: Lista de Compras**
- Clique em "Adicionar"
- Prefixo: `compras`
- Atalho: `ctrl+shift+1`
- Descrição: `Lista de compras`
- Marque "Habilitar este atalho"
- Clique em "Salvar"

**Resultado:** Ao pressionar `Ctrl+Shift+1`, copia:
```
[compras-05.11.2025-20:35]
```

### **3. Atalhos Sugeridos para Funções do Sistema**

Como NADA é fixo, configure você mesmo:

**Refresh do Menu:**
- Prefixo: *(vazio)*
- Atalho: `ctrl+shift+r` ou `alt+r`
- Descrição: `Atualizar menu`

**Buscar no Histórico:**
- Prefixo: *(vazio)*
- Atalho: `ctrl+shift+f` ou `alt+f`
- Descrição: `Buscar histórico`

## 💡 Dicas

### **Evite Conflitos com Navegador**
- `Ctrl+Shift+R` = Hard refresh no navegador
- Use alternativas: `Alt+R`, `Ctrl+Alt+R`, `F5+Ctrl`, etc.

### **Organize por Contexto**
```
Trabalho:
- Ctrl+Shift+1 → projeto
- Ctrl+Shift+2 → reuniao
- Ctrl+Shift+3 → cliente

Pessoal:
- Alt+1 → compras
- Alt+2 → tarefas
- Alt+3 → estudos
```

### **Use Prefixos Descritivos**
✅ Bom: `projeto`, `reuniao`, `compras`
❌ Evite: `aaa`, `xxx`, `temp`

## 🎨 Combinações Disponíveis

- `Ctrl+Shift+[1-9]`
- `Ctrl+Shift+[A-Z]`
- `Ctrl+Alt+[qualquer tecla]`
- `Alt+[qualquer tecla]`
- `Ctrl+Shift+F1-F12`
- E muitas outras!

## 📁 Arquivo de Configuração

Os atalhos são salvos em `settings.json`:

```json
{
  "custom_shortcuts": [
    {
      "id": 1,
      "hotkey": "ctrl+shift+1",
      "prefix": "compras",
      "enabled": true,
      "description": "Lista de compras"
    }
  ]
}
```

## ❓ Perguntas Frequentes

**P: Posso ter múltiplos atalhos?**
R: Sim! Até 10 atalhos diferentes.

**P: O que acontece se eu usar um atalho já configurado?**
R: O sistema avisa e não permite duplicatas.

**P: Posso desabilitar temporariamente um atalho?**
R: Sim! Edite o atalho e desmarque "Habilitar este atalho".

**P: Como remover um atalho?**
R: Selecione na lista e clique em "Remover".

## 🎉 Aproveite Sua Liberdade!

Configure do seu jeito! 🚀
