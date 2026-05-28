# ✅ Checklist de Pre-Deployment

Use este checklist para garantir que seu projeto está pronto para produção.

## 🔐 Segurança

- [ ] `SECRET_KEY` foi alterada (não use a padrão)
  ```bash
  python generate_secret_key.py
  ```

- [ ] `DEBUG = False` configurado em produção

- [ ] `.env` não está no git
  - Verifique `.gitignore`
  - Use `git rm --cached .env` se já foi commited

- [ ] Credenciais sensíveis não estão no código
  - SERVICE_TOKEN
  - USER_ID
  - XIAOMI_CHATBOT_PH

- [ ] CORS_ALLOWED_ORIGINS está restrito a domínios conhecidos
  - Não use `*` em produção

## 📦 Dependências

- [ ] `requirements.txt` atualizado
  ```bash
  pip freeze > requirements.txt
  ```

- [ ] `package.json` atualizado
  ```bash
  npm install
  npm list
  ```

- [ ] Nenhuma vulnerabilidade conhecida
  ```bash
  npm audit
  pip check
  ```

## 🏗️ Build

- [ ] Build frontend funciona localmente
  ```bash
  npm run build:frontend
  ```

- [ ] Frontend build é otimizado
  - Verificar `vite.config.js`
  - Verificar source maps desativados

- [ ] Static files de Django coletados
  ```bash
  python manage.py collectstatic --noinput
  ```

## 🌐 Configuração

- [ ] `ALLOWED_HOSTS` configurado corretamente
  - Inclua seu domínio Netlify
  - Inclua seu domínio customizado (se houver)

- [ ] `CORS_ALLOWED_ORIGINS` configurado
  - URL do Netlify
  - URL do domínio customizado (se houver)

- [ ] Variáveis de ambiente no Netlify
  - Vá para Site Settings → Environment
  - Adicione todas as variáveis do `.env`

- [ ] Variáveis de ambiente no Railway
  - Vá para Project → Variables
  - Adicione todas as variáveis necessárias

## 🗄️ Database

- [ ] Migrações executadas
  ```bash
  python manage.py migrate
  ```

- [ ] Nenhuma migração pendente
  ```bash
  python manage.py showmigrations
  ```

- [ ] Backup do banco local antes de deploy

## 📝 Documentação

- [ ] README.md está atualizado

- [ ] DEPLOY.md está completo

- [ ] Instruções estão claras

## 🚀 Deployment - Backend (Railway)

- [ ] Railway conectado ao repositório GitHub

- [ ] Build command configurado
  ```
  pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
  ```

- [ ] Start command configurado
  ```
  gunicorn xiaomi_proxy.wsgi:application --bind 0.0.0.0:$PORT
  ```

- [ ] Todas as variáveis de ambiente adicionadas

- [ ] Domain/URL do Railway anotado
  - Exemplo: `https://seu-app.railway.app`

## 🎨 Deployment - Frontend (Netlify)

- [ ] Netlify conectado ao repositório GitHub

- [ ] Build command: `npm run build:frontend`

- [ ] Publish directory: `dist`

- [ ] API URL no `netlify.toml` aponta para Railway
  ```toml
  [[redirects]]
    from = "/api/*"
    to = "https://seu-app.railway.app/api/:splat"
  ```

- [ ] Ambiente de produção configurado

- [ ] Build preview funcionando

## 🧪 Testes Pré-Deploy

### Backend (Railway)
- [ ] Acesse `/api/docs` para ver documentação
- [ ] Teste um endpoint manualmente
- [ ] Verifique logs no painel Railway

### Frontend (Netlify)
- [ ] Site carrega sem erros
- [ ] Abra Console (F12) e procure por erros
- [ ] Teste a comunicação com a API

### Integração
- [ ] API responde corretamente para requisições do frontend
- [ ] CORS não gera erros
- [ ] Dados são exibidos corretamente

## 📊 Monitoramento

- [ ] Logs configurados no Railway
- [ ] Alertas configurados (opcional)
- [ ] Erro tracking ativado (Sentry, etc)

## 🔄 Pós-Deployment

- [ ] Verificar Analytics do Netlify
- [ ] Monitorar uso do Railway
- [ ] Testar aplicação em diferentes navegadores
- [ ] Testar em dispositivos móveis
- [ ] Monitorar performance

## 💾 Backup e Recuperação

- [ ] Backup automático do database configurado
- [ ] Plano de recuperação documentado
- [ ] Contato de suporte guardado

---

**Antes de fazer deploy em produção:**

1. Marque todos os itens deste checklist ✅
2. Teste localmente com `npm run dev`
3. Verifique os logs após o deploy
4. Tenha um plano de rollback

**Sucesso no deployment! 🎉**
