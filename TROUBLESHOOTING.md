# 🆘 Troubleshooting - Netlify + Django

## 🔴 Frontend não carrega

### ❌ Erro: "Failed to fetch"
**Causa:** API backend não está acessível

**Solução:**
1. Verifique se backend está rodando no Railway
2. Verifique URL em `netlify.toml` - substitua `seu-app` por seu domínio real
3. No console do navegador (F12), procure por URLs de API bloqueadas

```toml
# netlify.toml - CORRETO
[[redirects]]
  from = "/api/*"
  to = "https://seu-app-real.railway.app/api/:splat"
```

### ❌ Erro: "CORS error"
**Causa:** Backend não permite requisições de sua origem

**Solução:**
1. Vá ao Railway e verifique variável `CORS_ALLOWED_ORIGINS`
2. Certifique-se que inclui sua URL Netlify:
```
CORS_ALLOWED_ORIGINS=https://seu-dominio.netlify.app,https://seu-dominio.com
```
3. Redeploy no Railway após alterar

### ❌ Erro: "404 Not Found"
**Causa:** Frontend ou build incorretos

**Solução:**
```bash
# Verifique se build funciona localmente
npm run build:frontend

# Verifique se pasta dist/ foi criada
ls dist/

# Verifique index.html em dist/
cat dist/index.html
```

---

## 🔴 Backend (Railway) não responde

### ❌ Erro 502/503
**Causa:** Aplicação Django não está rodando

**Solução:**
1. Acesse painel Railway → seu projeto
2. Verifique logs para erros
3. Verifique se variáveis de ambiente estão corretas
4. Re-deploy:
```
git push origin main
```

### ❌ Erro: "ModuleNotFoundError"
**Causa:** Dependências não instaladas

**Solução:**
1. Verifique se `requirements.txt` está no repositório
2. Verifique se build command em Railway é:
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### ❌ Erro de Banco de Dados
**Causa:** Migrações não rodaram

**Solução:**
1. Verifique os logs no Railway
2. Adicione variável: `DATABASE_URL` (Railroad fornece automaticamente)
3. Verifique se `python manage.py migrate` está no build command

---

## 🔴 CORS Errors

### ❌ "Access to XMLHttpRequest blocked by CORS policy"

**Passo 1: Verifique o Header**
No navegador (F12):
```javascript
// Console
fetch('https://seu-app.railway.app/api/seu-endpoint', {
  headers: {
    'Origin': window.location.origin
  }
}).then(r => console.log(r.headers.get('Access-Control-Allow-Origin')))
```

**Passo 2: Atualize Django**
Em seu servidor Railway, verifique `xiaomi_proxy/settings.py`:
```python
CORS_ALLOWED_ORIGINS = ['https://seu-dominio.netlify.app']
CORS_ALLOW_CREDENTIALS = True
```

**Passo 3: Redeploy**
```bash
git add .
git commit -m "Fix CORS"
git push
```

---

## 🔴 Problemas de Build

### ❌ Build falha no Netlify
**Solução:**
1. Acesse painel Netlify → seu site → Deploys
2. Clique no deploy falhado
3. Verifique logs para erro específico
4. Erros comuns:
```bash
# npm não encontrou módulo
npm install

# Python dependencies faltando
pip install -r requirements.txt

# Port já em uso
kill $(lsof -t -i :8000)
```

### ❌ Build é lento
**Causa:** Muitas dependências ou código grande

**Solução:**
1. Otimize o build em `vite.config.js`
2. Remova pacotes não usados
3. Use `npm audit` para identificar problemas

---

## 🔴 Problemas de Variáveis de Ambiente

### ❌ Variáveis não carregadas no Netlify
**Solução:**
1. Vá para: Site settings → Environment variables
2. Adicione manualmente cada variável
3. Redeploy após adicionar

**Verificar valores:**
```javascript
// Em src/App.jsx ou similar
console.log(import.meta.env.VITE_API_URL)
```

### ❌ Variáveis não carregadas no Railway
**Solução:**
1. Vá para: Project → Variables
2. Adicione ou atualize
3. Redeploy automático

**Verificar no console Django:**
```python
python manage.py shell
from django.conf import settings
print(settings.CORS_ALLOWED_ORIGINS)
```

---

## 🔴 Problemas de Performance

### ❌ Site lento
**Otimizações:**
```bash
# Build otimizado
npm run build:frontend  # já usa minificação

# Comprimir com gzip (automático no Netlify)
# Já está configurado em netlify.toml
```

### ❌ API lenta
**Solução:**
1. Adicione caching em Django
2. Otimize queries do banco
3. Use CDN para assets

---

## 🔴 Problemas com SSL/HTTPS

### ❌ "Mixed Content" error
**Causa:** Requisições HTTP para HTTPS

**Solução:**
```toml
# netlify.toml
[build]
  environment = { NODE_ENV = "production" }

# Força HTTPS
[[redirects]]
  from = "http://*"
  to = "https://:splat"
  status = 301
  force = true
```

---

## 🔴 Problemas de Segurança

### ❌ "Insecure credentials"
**Solução:**
1. Nunca commite `.env` com credenciais reais
2. Use variáveis de ambiente em Netlify/Railway
3. Regenere qualquer credencial exposta

```bash
python generate_secret_key.py
```

---

## ✅ Checklist de Debugging

Quando algo não funciona:

- [ ] Frontend carrega? (verifique Network tab)
- [ ] API responde? (teste com curl/Postman)
- [ ] CORS headers presentes? (verifique Response headers)
- [ ] Variáveis de ambiente setadas? (check Netlify + Railway)
- [ ] Build local funciona? (npm run build:frontend)
- [ ] Logs verificados? (Netlify Deploys + Railway)
- [ ] Credenciais válidas? (especialmente Xiaomi API)

---

## 🔧 Comandos de Debug

### Testar API com curl
```bash
curl -H "Origin: https://seu-dominio.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS \
  https://seu-app.railway.app/api/seu-endpoint \
  -v
```

### Verificar certificado SSL
```bash
curl -v https://seu-app.railway.app/api/ping
```

### Monitorar logs Railway em tempo real
```bash
# Acesse painel Railway e veja "Logs"
```

---

## 📞 Obter Ajuda

1. **Netlify Docs**: https://docs.netlify.com
2. **Railway Docs**: https://docs.railway.app
3. **Django CORS**: https://github.com/adamchainz/django-cors-headers
4. **Stack Overflow**: Tag `netlify` + `django`

---

## 🎯 Passo a Passo Completo de Debug

1. **Abra DevTools (F12)**
   - Aba "Network" → procure por requisições `/api/*`
   - Aba "Console" → procure por erros vermelhos

2. **Verifique status do backend**
   ```bash
   # Tente acessar diretamente
   curl https://seu-app.railway.app/api/docs
   ```

3. **Verifique CORS headers**
   - Na aba Network, clique na requisição
   - Vá em "Response Headers"
   - Procure por `access-control-allow-origin`

4. **Se nada funcionou:**
   - Re-leia [DEPLOY.md](DEPLOY.md)
   - Verifique [CHECKLIST.md](CHECKLIST.md)
   - Tente tudo localmente com `npm run dev`

---

**Última dica:** 99% dos problemas são CORS ou variáveis de ambiente 🎯
