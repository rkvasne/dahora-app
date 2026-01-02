# Como Atualizar Releases via API com GitHub Token

## 🔑 Passo 1: Gerar um Token de Acesso Pessoal

1. Vá para: https://github.com/settings/tokens?type=pat
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Dê um nome: `Dahora Release Updates`
4. Selecione as permissões (marque):
   - ✅ `repo` (Controle total de repositórios privados e públicos)
   - ✅ `workflow` (Atualizar workflows do GitHub Actions)

5. Clique em **"Generate token"**
6. **COPIE o token** (só aparece uma vez!)

## 📝 Passo 2: Salvar o Token Localmente

Crie um arquivo com o token:

```powershell
# Em PowerShell como Admin:
$token = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Cole o token aqui
$token | Out-File -FilePath "$HOME\.github_token" -Encoding UTF8
Write-Host "✅ Token salvo em: $HOME\.github_token"
```

## 🚀 Passo 3: Executar o Script de Atualização

```powershell
cd e:\Dahora\dahora-app
powershell -ExecutionPolicy Bypass -File scripts\update-releases.ps1
```

## ✅ Resultado

Se tudo der certo, você verá:
```
🔄 Atualizando v0.2.4...
✅ v0.2.4 atualizada com sucesso!
✅ v0.2.3 atualizada com sucesso!
... (e mais releases)
✨ Atualização concluída!
```

## ⚠️ Segurança

- **NÃO compartilhe o token** com ninguém
- O arquivo `.github_token` está no `.gitignore` (não será commitado)
- Você pode revogar o token depois em: https://github.com/settings/tokens

## 🔗 Links Úteis

- [Gerar Token](https://github.com/settings/tokens?type=pat)
- [Documentação de Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

---

**Próximos passos:**

1. Gere um token em: https://github.com/settings/tokens?type=pat
2. Execute: `powershell -ExecutionPolicy Bypass -File scripts\update-releases.ps1`
3. Pronto! Todas as releases serão atualizadas automaticamente 🎉
