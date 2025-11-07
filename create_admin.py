# create_admin_fixed.py
# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash
import psycopg2
import sys

def create_admin_user():
    """Cria o usuário admin com senha correta"""
    try:
        # Configuração direta
        conn = psycopg2.connect(
            host='localhost',
            database='gepat_db',
            user='gepat_user',
            password='gepat123',
            port='5432',
            client_encoding='UTF8'
        )
        
        cur = conn.cursor()
        
        # Gerar hash da senha 'admin123'
        password_hash = generate_password_hash('admin123')
        print(f"Hash gerado: {password_hash}")
        
        # Verificar se usuário já existe
        cur.execute("SELECT id FROM usuarios WHERE username = 'admin'")
        existing_user = cur.fetchone()
        
        if existing_user:
            # Atualizar senha
            cur.execute(
                "UPDATE usuarios SET password_hash = %s WHERE username = 'admin'",
                (password_hash,)
            )
            print("✅ Senha do admin atualizada!")
        else:
            # Criar novo usuário
            cur.execute('''
                INSERT INTO usuarios (username, password_hash, nome_completo, email) 
                VALUES ('admin', %s, 'Administrador', 'admin@gepat.com')
            ''', (password_hash,))
            print("✅ Usuário admin criado!")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("👉 Use: admin / admin123 para fazer login")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\nExecute estes comandos MANUALMENTE no pgAdmin:")
        print("""
-- Conectar ao banco gepat_db
\\c gepat_db;

-- Inserir usuário admin
INSERT INTO usuarios (username, password_hash, nome_completo, email) 
VALUES ('admin', 'pbkdf2:sha256:260000$ABC123$xyz789abcdef1234567890abcdef1234567890abcdef1234567890abcdef12', 'Administrador', 'admin@gepat.com')
ON CONFLICT (username) DO UPDATE SET 
password_hash = EXCLUDED.password_hash;
        """)
        return False

if __name__ == '__main__':
    # Configurar encoding no Windows
    if sys.platform == "win32":
        import os
        os.system('chcp 65001 > nul')
    
    create_admin_user()