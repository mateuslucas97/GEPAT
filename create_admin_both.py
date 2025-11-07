# create_admin_apoio_fixed.py
from werkzeug.security import generate_password_hash
import psycopg2
from config import Config

def create_admin_apoio_logistico():
    print("--- Criando admin no Apoio Logístico ---")
    
    config = Config.get_config('apoio_logistico')
    
    try:
        conn = psycopg2.connect(
            host=config['DB_HOST'],
            database=config['DB_NAME'],
            user=config['DB_USER'],  # Use um usuário com permissões
            password=config['DB_PASSWORD'],
            port=config['DB_PORT']
        )
        
        cur = conn.cursor()
        
        # Verificar se admin já existe
        cur.execute("SELECT id, username FROM usuarios WHERE username = 'admin'")
        admin_exists = cur.fetchone()
        
        if admin_exists:
            print(f"✅ Admin já existe (ID: {admin_exists[0]}, Username: {admin_exists[1]})")
            
            # Atualizar senha
            password_hash = generate_password_hash('admin123')
            cur.execute(
                "UPDATE usuarios SET password_hash = %s WHERE username = 'admin'",
                (password_hash,)
            )
            print("✅ Senha do admin atualizada")
        else:
            # Criar admin
            password_hash = generate_password_hash('admin123')
            cur.execute(
                "INSERT INTO usuarios (username, password_hash, nome_completo, email, ativo) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                ('admin', password_hash, 'Administrador', 'admin@gepat.com', True)
            )
            new_id = cur.fetchone()[0]
            print(f"✅ Admin criado (ID: {new_id})")
        
        # Verificar todos os usuários
        cur.execute("SELECT id, username, ativo FROM usuarios ORDER BY id")
        users = cur.fetchall()
        print(f"📊 Usuários existentes: {len(users)}")
        for user in users:
            print(f"   ID: {user[0]}, Username: {user[1]}, Ativo: {user[2]}")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Processo concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    create_admin_apoio_logistico()