#!/usr/bin/env python3
"""
Script para visualizar usuários cadastrados no Sustain 4.0 BioEngine
"""

import yaml
from datetime import datetime

def view_users():
    """Visualiza usuários cadastrados no sistema"""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        users = config.get('credentials', {}).get('usernames', {})
        
        print("🌿 SUSTAIN 4.0 BIOENGINE - USUÁRIOS CADASTRADOS")
        print("=" * 60)
        print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📊 Total de usuários: {len(users)}")
        print("=" * 60)
        
        if not users:
            print("❌ Nenhum usuário encontrado!")
            return
        
        for i, (username, user_data) in enumerate(users.items(), 1):
            # Determinar tipo de usuário
            user_type = "👑 Administrador" if username == 'admin' else "👤 Usuário"
            
            print(f"\n{i}. {user_type}")
            print(f"   Username: {username}")
            print(f"   Nome: {user_data.get('name', 'N/A')}")
            print(f"   Email: {user_data.get('email', 'N/A')}")
            print(f"   Senha Hash: {user_data.get('password', 'N/A')[:30]}...")
            print(f"   Status: 🟢 Ativo")
            
            if i < len(users):
                print("   " + "-" * 50)
        
        print("\n" + "=" * 60)
        
        # Estatísticas
        admin_count = sum(1 for u in users.keys() if u == 'admin')
        regular_users = len(users) - admin_count
        
        print("📈 ESTATÍSTICAS:")
        print(f"   • Administradores: {admin_count}")
        print(f"   • Usuários regulares: {regular_users}")
        print(f"   • Total: {len(users)}")
        
        # Informações do arquivo
        print(f"\n📄 Arquivo de configuração: config.yaml")
        print("🔒 Todas as senhas estão hasheadas com bcrypt para segurança")
        
    except FileNotFoundError:
        print("❌ Erro: Arquivo 'config.yaml' não encontrado!")
        print("   Certifique-se de que está no diretório correto do projeto.")
        
    except yaml.YAMLError as e:
        print(f"❌ Erro ao ler o arquivo YAML: {e}")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def list_usernames_only():
    """Lista apenas os usernames (formato simplificado)"""
    try:
        with open('config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        users = config.get('credentials', {}).get('usernames', {})
        
        print("📝 LISTA RÁPIDA DE USERNAMES:")
        print("-" * 30)
        for username in users.keys():
            print(f"• {username}")
        print(f"\nTotal: {len(users)} usuários")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--simple":
        list_usernames_only()
    else:
        view_users()
        
    input("\n⏸️  Pressione Enter para fechar...")
