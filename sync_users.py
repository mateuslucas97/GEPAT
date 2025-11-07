# sync_users.py
import psycopg2
from werkzeug.security import generate_password_hash
from config import Config

def sync_users_between_dbs():
    print("Sincronizando usuários entre bancos...")
    
    # Banco origem (TI)
    config_ti = Config.get_config('ti')
    
    try:
        # Conectar ao banco de TI
        conn_ti = psycopg2.connect(
            host=config_ti['DB_HOST'],
            database=config_ti['DB_NAME'],
            user=config_ti['DB_USER'],
            password=config_ti['DB_PASSWORD'],
            port=config_ti['DB_PORT']
        )
        
        cur_ti = conn_ti.cursor()
        cur_ti.execute('SELECT username, password_hash, nome_completo, email, ativo FROM usuarios')
        usuarios_ti = cur_ti.fetchall()
        
        print(f"Usuários no TI: {len(usuarios_ti)}")
        
        # Para cada banco destino
        bancos_destino = ['apoio_logistico']
        
        for setor_destino in bancos_destino:
            config_destino = Config.get_config(setor_destino)
            
            try:
                conn_destino = psycopg2.connect(
                    host=config_destino['DB_HOST'],
                    database=config_destino['DB_NAME'],
                    user=config_destino['DB_USER'],
                    password=config_destino['DB_PASSWORD'],
                    port=config_destino['DB_PORT']
                )
                
                cur_destino = conn_destino.cursor()
                
                # Verificar usuários existentes no destino
                cur_destino.execute('SELECT username FROM usuarios')
                usuarios_existentes = [row[0] for row in cur_destino.fetchall()]
                
                usuarios_adicionados = 0
                usuarios_atualizados = 0
                
                for usuario in usuarios_ti:
                    username, password_hash, nome_completo, email, ativo = usuario
                    
                    if username in usuarios_existentes:
                        # Atualizar usuário existente
                        cur_destino.execute(
                            'UPDATE usuarios SET password_hash = %s, nome_completo = %s, email = %s, ativo = %s WHERE username = %s',
                            (password_hash, nome_completo, email, ativo, username)
                        )
                        usuarios_atualizados += 1
                    else:
                        # Inserir novo usuário
                        cur_destino.execute(
                            'INSERT INTO usuarios (username, password_hash, nome_completo, email, ativo) VALUES (%s, %s, %s, %s, %s)',
                            (username, password_hash, nome_completo, email, ativo)
                        )
                        usuarios_adicionados += 1
                
                conn_destino.commit()
                cur_destino.close()
                conn_destino.close()
                
                print(f"✅ {setor_destino}: {usuarios_adicionados} adicionados, {usuarios_atualizados} atualizados")
                
            except Exception as e:
                print(f"❌ Erro no {setor_destino}: {e}")
        
        cur_ti.close()
        conn_ti.close()
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == '__main__':
    sync_users_between_dbs()