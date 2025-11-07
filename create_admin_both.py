# create_admin_both.py
from werkzeug.security import generate_password_hash
import psycopg2
from config import Config

def create_admin_in_both():
    bancos = ['ti', 'apoio_logistico']
    
    for setor in bancos:
        config = Config.get_config(setor)
        print(f"\n--- Configurando banco: {config['NOME']} ---")
        
        try:
            conn = psycopg2.connect(
                host=config['DB_HOST'],
                database=config['DB_NAME'],
                user=config['DB_USER'],
                password=config['DB_PASSWORD'],
                port=config['DB_PORT']
            )
            
            cur = conn.cursor()
            
            # Verificar se admin já existe
            cur.execute("SELECT id FROM usuarios WHERE username = 'admin'")
            admin_exists = cur.fetchone()
            
            if admin_exists:
                print(f"✅ Admin já existe no {config['NOME']}")
                
                # Atualizar senha para garantir que está correta
                password_hash = generate_password_hash('admin123')
                cur.execute(
                    "UPDATE usuarios SET password_hash = %s WHERE username = 'admin'",
                    (password_hash,)
                )
                print(f"✅ Senha do admin atualizada no {config['NOME']}")
            else:
                # Criar admin
                password_hash = generate_password_hash('admin123')
                cur.execute(
                    "INSERT INTO usuarios (username, password_hash, nome_completo, email) VALUES (%s, %s, %s, %s)",
                    ('admin', password_hash, 'Administrador', 'admin@gepat.com')
                )
                print(f"✅ Admin criado no {config['NOME']}")
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Erro no {config['NOME']}: {e}")

if __name__ == '__main__':
    create_admin_in_both()