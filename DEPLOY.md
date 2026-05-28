# Guia de Deploy - Netlify + Django

## 🚀 Resumo da Configuração

Este projeto consiste em:
- **Frontend**: React + Vite → Deploy no Netlify
- **Backend**: Django + Django-Ninja → Deploy em serviço serverless (Railway, Render, etc.)

## 📋 Pré-requisitos

- Node.js >= 18
- Python 3.11+
- Git
- Conta no Netlify
- Conta em Railway/Render (para o backend)

## 🔧 Passo 1: Preparar o Backend

### 1.1 Instalar Dependências
```bash
pip install -r requirements.txt
```

### 1.2 Configurar Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:
```bash
cp .env.example .env
```

**Variáveis obrigatórias:**
- `SECRET_KEY`: Gere uma nova chave segura
- `SERVICE_TOKEN`: Token da API Xiaomi
- `USER_ID`: ID do usuário Xiaomi
- `XIAOMI_CHATBOT_PH`: Identificador do chatbot
- `XIAOMI_MODEL_NAME`: Nome do modelo (ex: mimo-v2.5-pro)
- `XIAOMI_API_URL`: URL da API Xiaomi

### 1.3 Executar Migrações (se necessário)
```bash
python manage.py migrate
```

### 1.4 Coletar Static Files
```bash
python manage.py collectstatic --noinput
```

## 🚀 Passo 2: Deploy do Backend (Railway)

### 2.1 Criar Conta e Projeto
1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Crie um novo projeto

### 2.2 Conectar Repositório
1. Selecione "Deploy from GitHub"
2. Autorize e selecione seu repositório
3. Configure as variáveis de ambiente no painel do Railway

### 2.3 Configurar Variáveis
No painel do Railway:
```
DEBUG=False
SECRET_KEY=sua-chave-segura
ALLOWED_HOSTS=seu-app.railway.app,seu-dominio.com
CORS_ALLOWED_ORIGINS=https://seu-netlify-domain.netlify.app
SERVICE_TOKEN=seu-token
USER_ID=seu-user-id
XIAOMI_CHATBOT_PH=seu-ph
XIAOMI_MODEL_NAME=seu-modelo
XIAOMI_API_URL=https://aistudio.xiaomimimo.com/open-apis/bot/chat
```

### 2.4 Obtém URL do Backend
Railway fornecerá uma URL como: `https://seu-app.railway.app`

## 🎨 Passo 3: Deploy do Frontend (Netlify)

### 3.1 Configurar URL da API
Atualize a URL da API no código React. Procure por variáveis como `VITE_API_URL` ou similar e defina:
```javascript
const API_URL = 'https://seu-app.railway.app/api';
```

Ou use uma variável de ambiente:
```bash
VITE_API_URL=https://seu-app.railway.app/api
```

### 3.2 Atualizar netlify.toml
Abra `netlify.toml` e atualize a URL do backend:
```toml
[[redirects]]
  from = "/api/*"
  to = "https://seu-app.railway.app/api/:splat"
  status = 200
  force = false
```

### 3.3 Deploy no Netlify
```bash
npm install
npm run build:frontend
```

Depois, conecte ao Netlify:
1. Acesse [netlify.com](https://netlify.com)
2. Clique "Add new site" → "Import an existing project"
3. Selecione seu repositório GitHub
4. Configure:
   - Build command: `npm run build:frontend`
   - Publish directory: `dist`
5. Clique "Deploy site"

### 3.4 Configurar Variáveis de Ambiente no Netlify
No painel do Netlify, vá para "Site settings" → "Environment variables" e adicione:
```
VITE_API_URL=https://seu-app.railway.app/api
```

## ✅ Verificações Finais

### Testar CORS
```bash
curl -X OPTIONS https://seu-app.railway.app/api/seu-endpoint \
  -H "Origin: https://seu-netlify-domain.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

### Testar Conectividade
1. Acesse seu site Netlify
2. Abra o Console do Navegador (F12)
3. Faça uma requisição para a API
4. Verifique se há erros de CORS

## 🐛 Solução de Problemas

### Erro 503 no Backend
- Verifique se o serviço está rodando no Railway
- Confirme as variáveis de ambiente

### Erro CORS
- Verifique `CORS_ALLOWED_ORIGINS` no backend
- Certifique-se de que a URL do Netlify está listada
- Verifique os headers em `netlify.toml`

### Build falha no Netlify
- Verifique se `npm run build:frontend` funciona localmente
- Confirme que todas as dependências estão em `package.json`
- Verifique os logs do build no painel Netlify

### API não responde
- Verifique se a URL do backend em `netlify.toml` está correta
- Confirme que o backend está rodando
- Verifique os logs de erro no Railway

## 📚 Recursos Úteis

- [Documentação Netlify](https://docs.netlify.com)
- [Documentação Railway](https://docs.railway.app)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)
- [Django Ninja](https://django-ninja.rest-framework.com)

## 🔐 Checklist de Segurança para Produção

- [ ] `SECRET_KEY` alterada e segura
- [ ] `DEBUG = False` em produção
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] HTTPS ativado em ambos os serviços
- [ ] CORS restrito a domínios conhecidos
- [ ] Credenciais Xiaomi seguras (não commitar no git)
- [ ] `.env` adicionado ao `.gitignore`
- [ ] Database backup configurado
- [ ] Logging e monitoramento ativados
