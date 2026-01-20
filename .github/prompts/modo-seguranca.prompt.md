---
description: Segurança aplicada — auditoria OWASP, análise de exposições, recomendações de mitigação e boas práticas de logging
---

# Modo Segurança

> Carregue este arquivo quando precisar revisar ou implementar segurança.
> Baseado em **OWASP Top 10:2025** e melhores práticas da indústria.

---

## 🎯 Quando Usar

- Revisão de código com foco em segurança
- Implementação de autenticação/autorização
- Proteção de dados sensíveis
- Configuração de APIs seguras
- Auditoria de vulnerabilidades OWASP Top 10

---

## 🛡️ OWASP Top 10:2025 - Referência Rápida

1. **A01** - Broken Access Control
2. **A02** - Security Misconfiguration
3. **A03** - Software Supply Chain Failures
4. **A04** - Cryptographic Failures
5. **A05** - Injection
6. **A06** - Insecure Design
7. **A07** - Authentication Failures
8. **A08** - Software/Data Integrity Failures
9. **A09** - Security Logging/Alerting Failures
10. **A10** - Mishandling of Exceptional Conditions

---

## 🔐 A01:2025 - Broken Access Control

**#1 no OWASP Top 10** - 100% de aplicações testadas têm alguma forma de controle de acesso quebrado.

### Princípios
```typescript
// ✅ Deny by Default - negue tudo, permita apenas o necessário
const permissions = {
  admin: ['read', 'write', 'delete', 'manage_users'],
  editor: ['read', 'write'],
  viewer: ['read'],
}

// ✅ Middleware de autorização em CADA endpoint
function authorize(requiredPermission: string) {
  return (req, res, next) => {
    const userRole = req.user?.role
    const userPermissions = permissions[userRole] || []
    
    if (!userPermissions.includes(requiredPermission)) {
      return res.status(403).json({ error: 'Acesso negado' })
    }
    next()
  }
}

// ✅ Verificar propriedade do recurso
app.delete('/api/posts/:id', authorize('delete'), async (req, res) => {
  const post = await Post.findById(req.params.id)
  
  // Regra: apenas dono ou admin pode deletar
  if (post.authorId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Não autorizado' })
  }
  
  await post.delete()
  res.json({ success: true })
})
[markdown]

### Vulnerabilidades Comuns (CWEs)
- ❌ **CWE-352** - CSRF
- ❌ **CWE-862** - Missing Authorization
- ❌ **CWE-863** - Incorrect Authorization
- ❌ **CWE-918** - SSRF
- ❌ **CWE-200** - Exposure of Sensitive Information

### Prevenção
- ✅ Deny by default em TODOS os recursos
- ✅ Implemente access control uma vez, reutilize
- ✅ Minimize uso de CORS
- ✅ Invalide sessões no logout
- ✅ Use tokens JWT de curta duração
- ✅ Log de falhas de acesso + alertas
- ✅ Rate limiting em APIs

---

## 🔐 Validação e Sanitização

### Validação de Entrada
```typescript
// ✅ Valide no cliente E no servidor
// Cliente: feedback rápido
// Servidor: segurança real

// ✅ Use schemas de validação
import { z } from 'zod'

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
  age: z.number().min(18).max(120),
})

// ✅ Liste branca > Lista negra
const allowedRoles = ['admin', 'user', 'guest']
if (!allowedRoles.includes(role)) throw new Error('Role inválido')
```

### Sanitização
```typescript
// ✅ Sanitize HTML para prevenir XSS
import DOMPurify from 'dompurify'
const safeHtml = DOMPurify.sanitize(userInput)

// ✅ Escape em diferentes contextos
// HTML: &lt; &gt; &amp;
// SQL: use queries parametrizadas
// JS: JSON.stringify para dados em scripts
```

---

## 🔑 Autenticação

### Senhas Seguras
```typescript
// ✅ Use bcrypt ou Argon2 para hash
import bcrypt from 'bcrypt'

const SALT_ROUNDS = 12
const hash = await bcrypt.hash(password, SALT_ROUNDS)
const isValid = await bcrypt.compare(password, hash)

// ✅ Requisitos de senha forte
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
```

### JWT e Sessões
```typescript
// ✅ JWT com expiração curta
const token = jwt.sign(payload, SECRET, { expiresIn: '15m' })

// ✅ Refresh tokens com rotação
const refreshToken = jwt.sign({ userId }, REFRESH_SECRET, { expiresIn: '7d' })

// ✅ Configuração segura de cookies
res.cookie('token', token, {
  httpOnly: true,      // Não acessível via JS
  secure: true,        // Apenas HTTPS
  sameSite: 'strict',  // Proteção CSRF
  maxAge: 15 * 60 * 1000
})
```

### Multi-Factor Authentication (MFA)
```typescript
// ✅ Implemente quando possível
// - TOTP (Google Authenticator)
// - SMS (menos seguro)
// - Email
// - WebAuthn/FIDO2 (mais seguro)
```

---

## 🛡️ Autorização

### RBAC (Role-Based Access Control)
```typescript
// ✅ Defina roles e permissões
const permissions = {
  admin: ['read', 'write', 'delete', 'manage_users'],
  editor: ['read', 'write'],
  viewer: ['read'],
}

// ✅ Middleware de autorização
function authorize(requiredPermission: string) {
  return (req, res, next) => {
    const userRole = req.user.role
    const userPermissions = permissions[userRole] || []
    
    if (!userPermissions.includes(requiredPermission)) {
      return res.status(403).json({ error: 'Acesso negado' })
    }
    next()
  }
}

// ✅ Verifique em cada operação, não só na rota
app.delete('/api/posts/:id', authorize('delete'), async (req, res) => {
  // Verifique também se o usuário é dono do recurso
  const post = await Post.findById(req.params.id)
  if (post.authorId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Não autorizado' })
  }
})
```

---

## 🔒 Proteção de Dados

### Dados em Trânsito
```typescript
// ✅ HTTPS obrigatório
// ✅ HSTS header
res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')

// ✅ TLS 1.2+ apenas
```

### Dados em Repouso
```typescript
// ✅ Criptografe dados sensíveis
import crypto from 'crypto'

const algorithm = 'aes-256-gcm'
const key = crypto.scryptSync(password, salt, 32)

function encrypt(text: string): string {
  const iv = crypto.randomBytes(16)
  const cipher = crypto.createCipheriv(algorithm, key, iv)
  // ...
}
```

### Gerenciamento de Segredos
```bash
# ✅ Variáveis de ambiente
DATABASE_URL=...
JWT_SECRET=...
API_KEY=...

# ✅ Nunca no código
const secret = process.env.JWT_SECRET  # ✅
const secret = 'my-secret-key'         # ❌

# ✅ Arquivos .env no .gitignore
```

---

## 🌐 Segurança de API

### Headers de Segurança
```typescript
// ✅ Helmet.js para Express
import helmet from 'helmet'
app.use(helmet())

// ✅ Headers manuais
res.setHeader('X-Content-Type-Options', 'nosniff')
res.setHeader('X-Frame-Options', 'DENY')
res.setHeader('X-XSS-Protection', '1; mode=block')
res.setHeader('Content-Security-Policy', "default-src 'self'")
```

### CORS
```typescript
// ✅ Origens específicas
app.use(cors({
  origin: ['https://meusite.com', 'https://app.meusite.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
}))

// ❌ Nunca em produção
app.use(cors({ origin: '*' }))
```

### Rate Limiting
```typescript
// ✅ Limite requisições
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // 100 requisições por IP
  message: 'Muitas requisições, tente novamente mais tarde',
})

// ✅ Limite mais restrito para auth
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hora
  max: 5, // 5 tentativas de login
})

app.use('/api/', limiter)
app.use('/api/auth/login', authLimiter)
```

---

## ⚠️ Vulnerabilidades Comuns

### SQL Injection
```typescript
// ❌ NUNCA concatene strings
const query = `SELECT * FROM users WHERE id = ${userId}` // PERIGOSO!

// ✅ Use queries parametrizadas
const query = 'SELECT * FROM users WHERE id = $1'
const result = await db.query(query, [userId])

// ✅ Ou use ORM
const user = await prisma.user.findUnique({ where: { id: userId } })
```

### XSS (Cross-Site Scripting)
```typescript
// ❌ Não renderize HTML de usuário diretamente
div.innerHTML = userInput // PERIGOSO!

// ✅ Use textContent
div.textContent = userInput

// ✅ Em React, já é escapado por padrão
<div>{userInput}</div> // Seguro

// ⚠️ Cuidado com dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: sanitizedHtml }} />
```

### CSRF (Cross-Site Request Forgery)
```typescript
// ✅ Token anti-CSRF
import csrf from 'csurf'
app.use(csrf({ cookie: true }))

// ✅ SameSite cookies
res.cookie('session', token, { sameSite: 'strict' })

// ✅ Verifique Origin/Referer para requisições críticas
```

---

## ✅ Checklist de Segurança

### Autenticação
- [ ] Senhas com hash seguro (bcrypt/Argon2)
- [ ] JWT com expiração curta
- [ ] Refresh tokens com rotação
- [ ] MFA disponível

### Autorização
- [ ] RBAC implementado
- [ ] Verificação em cada endpoint
- [ ] Princípio do menor privilégio

### Dados
- [ ] HTTPS em produção
- [ ] Dados sensíveis criptografados
- [ ] Segredos em variáveis de ambiente
- [ ] .env no .gitignore

### API
- [ ] Headers de segurança
- [ ] CORS configurado
- [ ] Rate limiting
- [ ] Validação de entrada


---

## ✅ Checklist de Segurança (referência)

- [ ] Revisar autenticação e autorização
- [ ] Validar e sanitizar todas as entradas
- [ ] Proteger dados sensíveis (criptografia, .env)
- [ ] Configurar headers de segurança e CORS
- [ ] Implementar rate limiting e logging
- [ ] Atualizar dependências e monitorar vulnerabilidades

**Referências:**
- [OWASP Top 10:2025](https://owasp.org/www-project-top-ten/)
- [Security Checklist](../../checklists/security-checklist.md)

## 💬 Frases para o Agente

```markdown
"Entre no modo segurança"
"Revise este código buscando vulnerabilidades"
"Implemente autenticação segura"
"Configure proteção CSRF"
"Verifique se há SQL injection"
```

---
