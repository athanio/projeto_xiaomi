#!/usr/bin/env python
"""
Script de setup para configuração rápida do projeto
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Executa um comando e mostra o progresso"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro!")
        print(e)
        return False

def setup():
    """Executa o setup completo"""
    print("""
    🤖 Xiaomi Proxy - Setup Inicial
    ================================
    
    Este script vai configurar o projeto para desenvolvimento local.
    """)
    
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    steps = [
        (
            f"{sys.executable} -m venv .venv",
            "Criando virtual environment"
        ),
        (
            f"{sys.executable} -m pip install --upgrade pip",
            "Atualizando pip"
        ),
        (
            f"{sys.executable} -m pip install -r requirements.txt",
            "Instalando dependências Python"
        ),
        (
            "npm install",
            "Instalando dependências Node.js"
        ),
        (
            f"{sys.executable} manage.py migrate",
            "Executando migrações Django"
        ),
    ]
    
    for cmd, description in steps:
        if not run_command(cmd, description):
            print(f"\n⚠️  Erro durante: {description}")
            print("Continue manualmente ou tente novamente.")
            return False
    
    # Criar .env se não existir
    env_file = base_dir / ".env"
    env_example = base_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print(f"\n{'='*60}")
        print("📝 Copiando .env.example para .env")
        print(f"{'='*60}")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Arquivo .env criado! Edite com suas credenciais.")
    
    # Gerar SECRET_KEY
    print(f"\n{'='*60}")
    print("🔐 Gerando SECRET_KEY")
    print(f"{'='*60}")
    try:
        result = subprocess.run([sys.executable, "generate_secret_key.py"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Erro ao gerar SECRET_KEY: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Setup completo!")
    print(f"{'='*60}")
    print("""
    Próximos passos:
    
    1. Edite o arquivo .env com suas credenciais:
       - SERVICE_TOKEN
       - USER_ID
       - XIAOMI_CHATBOT_PH
       - XIAOMI_MODEL_NAME
    
    2. Para rodar localmente:
       npm run dev
    
    3. Acesse:
       - Frontend: http://localhost:5173
       - Backend: http://localhost:8000
       - API Docs: http://localhost:8000/api/docs
    
    4. Para fazer deploy, leia DEPLOY.md
    """)
    
    return True

if __name__ == "__main__":
    try:
        success = setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Setup cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro durante setup: {e}")
        sys.exit(1)
