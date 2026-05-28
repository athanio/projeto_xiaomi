#!/usr/bin/env python
"""
Script de verificação pré-deploy
Valida se o projeto está pronto para deploy
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Executa comando e retorna sucesso/falha"""
    print(f"\n🔍 {description}...", end=" ")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            print("✅")
            return True
        else:
            print("❌")
            print(f"   Erro: {result.stderr or result.stdout}")
            return False
    except Exception as e:
        print(f"❌ ({str(e)})")
        return False

def main():
    print("""
    ╔════════════════════════════════════════════╗
    ║   🔍 PRÉ-DEPLOYMENT VALIDATION SCRIPT      ║
    ╚════════════════════════════════════════════╝
    """)

    checks = [
        ("npm ci --legacy-peer-deps", "Verificando Node.js dependencies"),
        ("npm run build:frontend", "Build frontend (Vite)"),
        ("python manage.py check", "Verificando Django settings"),
        ("python manage.py collectstatic --noinput --dry-run", "Validando static files"),
    ]

    passed = 0
    failed = 0

    for cmd, desc in checks:
        if run_command(cmd, desc):
            passed += 1
        else:
            failed += 1

    print(f"\n╔════════════════════════════════════════════╗")
    print(f"║   Resultado: {passed} ✅  {failed} ❌            ║")
    print(f"╚════════════════════════════════════════════╝")

    if failed == 0:
        print("\n🎉 Projeto pronto para deployment!")
        print("\nPróximos passos:")
        print("1. Commit suas mudanças: git add . && git commit -m 'Deploy ready'")
        print("2. Push para GitHub: git push origin main")
        print("3. Deploy no Netlify/Railway será automático")
        return 0
    else:
        print(f"\n⚠️  {failed} verificação(ões) falharam!")
        print("Corrija os erros acima antes de fazer deploy.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
