# fix_admin.py
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from config import Config

def fix_admin_password():
    try:
        # Conectar ao banco
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        
        cur = conn.cursor()
        
        # Gerar hash correto para 'admin123'
        new_password_hash = generate_password_hash('admin123')
        print(f"Novo hash gerado: {new_password_hash}")
        
        # Atualizar a senha do admin
        cur.execute(
            "UPDATE usuarios SET password_hash = %s WHERE username = 'admin'",
            (new_password_hash,)
        )
        
        # Verificar se funcionou
        cur.execute("SELECT password_hash FROM usuarios WHERE username = 'admin'")
        stored_hash = cur.fetchone()[0]
        
        # Testar se a senha funciona
        if check_password_hash(stored_hash, 'admin123'):
            print("✅ Senha do admin corrigida com sucesso!")
            print("👉 Agora use: admin / admin123")
        else:
            print("❌ Erro: A senha ainda não está correta")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == '__main__':
    fix_admin_password()