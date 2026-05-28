# Netlify Functions (Opcional)

## Nota
Esta pasta foi criada para referência futura, mas a configuração atual do projeto usa um backend Django em um serviço externo (Railway, Render, etc.) em vez de funções serverless no Netlify.

Se você quiser rodar o Django como uma Netlify Function no futuro, pode usar o arquivo `api.py` como base, mas isso requer configuração adicional e suporta limitações de serverless.

## Arquitetura Recomendada (Atual)
- **Frontend**: Netlify (React + Vite)
- **Backend**: Railway/Render (Django + Ninja API)

Isso oferece melhor desempenho e é mais fácil de manter do que tentar rodar Django como função serverless.
