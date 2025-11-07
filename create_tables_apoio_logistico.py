# create_tables_apoio_logistico_fixed.py
import psycopg2
from config import Config

def create_usuario_table_apoio_logistico():
    print("--- Criando tabela usuarios no Apoio Logístico ---")
    
    config = Config.get_config('apoio_logistico')
    
    try:
        conn = psycopg2.connect(
            host=config['DB_HOST'],
            database=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            port=config['DB_PORT']
        )
        
        cur = conn.cursor()
        
        # Primeiro, verificar e criar schema public se necessário
        cur.execute("CREATE SCHEMA IF NOT EXISTS public")
        print("✅ Schema 'public' verificado/criado")
        
        # Conceder permissões no schema
        cur.execute("GRANT ALL ON SCHEMA public TO public")
        print("✅ Permissões concedidas no schema public")
        
        # Criar tabela usuarios
        cur.execute('''
            CREATE TABLE IF NOT EXISTS public.usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                nome_completo VARCHAR(200),
                email VARCHAR(200),
                ativo BOOLEAN DEFAULT true,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("✅ Tabela 'usuarios' criada/verificada")
        
        # Garantir que a sequência está no schema correto
        cur.execute("CREATE SEQUENCE IF NOT EXISTS public.usuarios_id_seq START 1")
        print("✅ Sequência criada/verificada")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Estrutura criada com sucesso no Apoio Logístico")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

def verify_schema_and_tables():
    print("\n--- Verificando schema e tabelas ---")
    
    config = Config.get_config('apoio_logistico')
    
    try:
        conn = psycopg2.connect(
            host=config['DB_HOST'],
            database=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            port=config['DB_PORT']
        )
        
        cur = conn.cursor()
        
        # Verificar schemas existentes
        cur.execute("SELECT schema_name FROM information_schema.schemata")
        schemas = cur.fetchall()
        print(f"Schemas disponíveis: {[s[0] for s in schemas]}")
        
        # Verificar tabelas no schema public
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"Tabelas no schema public: {[t[0] for t in tables]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")

if __name__ == '__main__':
    create_usuario_table_apoio_logistico()
    verify_schema_and_tables()