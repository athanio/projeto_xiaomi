#!/usr/bin/env python
"""
Script para gerar uma SECRET_KEY segura para Django
"""
import secrets
import string

def generate_secret_key(length=50):
    """Gera uma chave secreta segura para Django"""
    allowed_chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    return secret_key

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print("SECRET_KEY gerada:")
    print(secret_key)
    print("\nCopie a chave acima e adicione ao .env:")
    print(f"SECRET_KEY={secret_key}")
