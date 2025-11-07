# init_apoio_logistico.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.security import generate_password_hash

def init_apoio_logistico():
    try:
        print("Inicializando banco do Apoio Logístico...")
        
        # Conectar ao PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='administrador',  # Altere se necessário
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Verificar se o banco existe
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'gepat_apoio_logistico'")
        exists = cur.fetchone()
        
        if not exists:
            print("Criando banco gepat_apoio_logistico...")
            cur.execute('CREATE DATABASE gepat_apoio_logistico')
            print("✅ Banco criado com sucesso!")
        else:
            print("✅ Banco já existe")
        
        cur.close()
        conn.close()
        
        print("✅ Inicialização do Apoio Logístico concluída!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    init_apoio_logistico()