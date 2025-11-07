# check_users.py
import psycopg2
from config import Config

def check_users_all_dbs():
    print("Verificando usuários em todos os bancos...")
    
    bancos = ['ti', 'apoio_logistico']
    
    for setor in bancos:
        config = Config.get_config(setor)
        
        try:
            conn = psycopg2.connect(
                host=config['DB_HOST'],
                database=config['DB_NAME'],
                user=config['DB_USER'],
                password=config['DB_PASSWORD'],
                port=config['DB_PORT']
            )
            
            cur = conn.cursor()
            cur.execute('SELECT id, username, nome_completo, ativo FROM usuarios ORDER BY id')
            usuarios = cur.fetchall()
            
            print(f"\n--- {config['NOME']} ({len(usuarios)} usuários) ---")
            for usuario in usuarios:
                status = "✅ Ativo" if usuario[3] else "❌ Inativo"
                print(f"  {usuario[0]}: {usuario[1]} - {usuario[2]} - {status}")
            
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Erro no {config['NOME']}: {e}")

if __name__ == '__main__':
    check_users_all_dbs()