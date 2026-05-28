# 🤖 Xiaomi Proxy - IFPI

Sistema de proxy inteligente para comunicação com IA Xiaomi. Combina um frontend React moderno com um backend Django robusto.

## 📸 Visualização Geral

- **Frontend**: React 18 + Vite + TailwindCSS
- **Backend**: Django 5.2 + Django-Ninja API
- **API Proxy**: Integração com API Xiaomi Mimo

## ✨ Características

- ✅ API REST moderna com Django-Ninja
- ✅ Frontend React responsivo com Vite
- ✅ CORS configurado para múltiplos ambientes
- ✅ Pronto para deploy no Netlify + Railway
- ✅ Variáveis de ambiente seguras
- ✅ Documentação de API automática (Swagger)

## 🚀 Quick Start

### Pré-requisitos
- Node.js >= 18
- Python 3.11+
- pip

### Instalação

1. **Clone o repositório**
```bash
git clone <seu-repo>
cd xiaomi_proxy
```

2. **Instale as dependências Python**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

3. **Instale as dependências Node.js**
```bash
npm install
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

5. **Execute localmente**
```bash
npm run dev
```

Isso iniciará:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## 📦 Estrutura do Projeto

```
xiaomi_proxy/
├── proxy/                  # App Django principal
│   ├── views.py           # Endpoints da API
│   ├── urls.py            # Rotas da API
│   ├── services/          # Lógica de negócio
│   └── models.py          # Modelos de dados
├── xiaomi_proxy/          # Configurações Django
│   ├── settings.py        # Configurações (CORS, DB, etc)
│   ├── urls.py            # URLs principais
│   └── wsgi.py            # WSGI application
├── src/                   # Frontend React
│   ├── components/        # Componentes React
│   ├── pages/            # Páginas da aplicação
│   └── App.jsx           # Componente raiz
├── public/               # Assets estáticos
├── package.json          # Dependências Node
├── requirements.txt      # Dependências Python
├── manage.py            # CLI Django
├── vite.config.js       # Configuração Vite
├── netlify.toml         # Configuração Netlify
└── DEPLOY.md            # Guia de deploy
```

## 🔧 Comandos Úteis

### Desenvolvimento
```bash
# Rodar tudo junto
npm run dev

# Apenas frontend
npm run dev:frontend

# Apenas backend
npm run dev:backend

# Preview do build
npm run preview
```

### Build
```bash
# Build frontend
npm run build:frontend

# Build completo
npm run build
```

### Django
```bash
# Migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar static files
python manage.py collectstatic

# Shell Django
python manage.py shell

# Gerar SECRET_KEY
python generate_secret_key.py
```

## 🌐 Variáveis de Ambiente

Veja [.env.example](.env.example) para lista completa.

**Essenciais:**
- `DEBUG`: True/False
- `SECRET_KEY`: Chave secreta Django
- `ALLOWED_HOSTS`: Hosts permitidos
- `CORS_ALLOWED_ORIGINS`: Origins CORS permitidos
- `SERVICE_TOKEN`: Token API Xiaomi
- `USER_ID`: ID do usuário Xiaomi
- `XIAOMI_API_URL`: URL da API Xiaomi

## 🚢 Deployment

### Desenvolvimento Local ✅
```bash
npm run dev
```

### Produção (Netlify + Railway)
Consulte [DEPLOY.md](DEPLOY.md) para instruções completas.

**Resumo:**
1. Deploy backend no Railway (leia DEPLOY.md)
2. Configure CORS no backend
3. Deploy frontend no Netlify
4. Atualize `netlify.toml` com URL do backend

## 📚 Documentação

- [Guia de Deploy](DEPLOY.md) - Instruções completo para produção
- [Django-Ninja](https://django-ninja.rest-framework.com/) - Framework API
- [Vite](https://vitejs.dev/) - Build tool frontend
- [Django Docs](https://docs.djangoproject.com/) - Documentação Django

## 🐛 Solução de Problemas

### CORS Error
- Verifique se URL está em `CORS_ALLOWED_ORIGINS`
- Reinicie o servidor Django após alterar

### Port já em uso
```bash
# Linux/Mac: Kill processo
lsof -ti :8000 | xargs kill -9

# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

### Build falha
```bash
# Limpe cache
rm -rf node_modules dist
npm install
npm run build:frontend
```

## 📝 Licença

[Sua licença aqui]

## 👤 Autor

IFPI - [seu-nome]

## 🤝 Contribuições

Contribuições são bem-vindas! Abra uma issue ou pull request.

---

**Última atualização**: Maio 2026
