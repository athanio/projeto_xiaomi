FROM python:3.11-slim

WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copie requirements e instale Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . .

# Exponha porta
EXPOSE 8000

# Colete static files
RUN python manage.py collectstatic --noinput

# Comando para rodar a aplicação
CMD ["gunicorn", "xiaomi_proxy.wsgi:application", "--bind", "0.0.0.0:8000"]
