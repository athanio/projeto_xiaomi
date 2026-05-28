# ⚡ QUICKSTART - Comandos Essenciais

## 🏃 Setup Rápido (Primeira vez)

```bash
# Opção 1: Automático (Recomendado)
python setup.py

# Opção 2: Manual
pip install -r requirements.txt
npm install
python manage.py migrate
```

## 🚀 Rodar Localmente

```bash
# Tudo junto (frontend + backend)
npm run dev

# Apenas frontend
npm run dev:frontend

# Apenas backend
npm run dev:backend
```

**Acesso:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

---

## 🔧 Configuração

### Editar Variáveis
```bash
# Copiar template
cp .env.example .env

# Editar com suas credenciais
# (VSCode abre automaticamente)
code .env
```

### Gerar Nova SECRET_KEY
```bash
python generate_secret_key.py
```

---

## 📦 Build & Deploy

### Build Frontend
```bash
npm run build:frontend
# Resultado em: dist/
```

### Coletar Static Files Django
```bash
python manage.py collectstatic --noinput
```

### Com Docker
```bash
# Build
docker build -t xiaomi-proxy .

# Rodar
docker run -p 8000:8000 xiaomi-proxy
```

---

## 🔍 Verificações

### Django Check
```bash
python manage.py check
```

### Dependencies Check
```bash
npm list
pip check
```

### Build Check
```bash
npm run build:frontend  # Deve gerar dist/
```

---

## 📚 Documentação

| Arquivo | Propósito |
|---------|-----------|
| [README.md](README.md) | Visão geral do projeto |
| [DEPLOY.md](DEPLOY.md) | **Guia completo de deployment** ⭐ |
| [CHECKLIST.md](CHECKLIST.md) | Verificações antes de deploy |
| [RESUMO.md](RESUMO.md) | O que foi configurado |

**👉 LEIA [DEPLOY.md](DEPLOY.md) ANTES DE FAZER DEPLOY! 👈**

---

## 🌐 URLs de Produção

Após deploy:
- **Frontend**: https://seu-dominio.netlify.app
- **Backend**: https://seu-app.railway.app
- **API**: https://seu-app.railway.app/api

---

## 🆘 Problemas Comuns

### Port 8000/5173 em uso
```powershell
# Windows
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

### Módulo não encontrado
```bash
pip install -r requirements.txt  # Python
npm install                      # Node
```

### Build falha
```bash
rm -rf dist node_modules
npm install
npm run build:frontend
```

### CORS error
- Verifique `CORS_ALLOWED_ORIGINS` em `.env`
- Reinicie o servidor Django

---

## 💡 Dicas

- Use `npm run dev` para desenvolvimento rápido
- Consulte API Docs em http://localhost:8000/api/docs
- Salve senhas do `.env` em lugar seguro
- Commit apenas código, não `.env`

---

**Pronto? Leia [DEPLOY.md](DEPLOY.md) para ir para produção! 🚀**
