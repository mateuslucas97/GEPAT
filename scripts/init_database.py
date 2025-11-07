# init_database.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.security import generate_password_hash
from config import Config

def init_databases():
    print("Inicializando bancos de dados GEPAT...")
    
    bancos = ['ti', 'apoio_logistico']
    
    for setor in bancos:
        config = Config.get_config(setor)
        print(f"\n--- Configurando {config['NOME']} ---")
        
        try:
            conn = psycopg2.connect(
                host=config['DB_HOST'],
                database=config['DB_NAME'],
                user=config['DB_USER'],
                password=config['DB_PASSWORD'],
                port=config['DB_PORT']
            )
            
            print(f"✅ Banco {config['DB_NAME']} conectado")
            
            # Verificar/criar tabelas
            cur = conn.cursor()
            
            tabelas_sql = [
                # Tabela usuarios
                '''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    nome_completo VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    ativo BOOLEAN DEFAULT TRUE,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''',
                
                # Tabela patrimonios
                '''
                CREATE TABLE IF NOT EXISTS patrimonios (
                    id SERIAL PRIMARY KEY,
                    numero_patrimonio VARCHAR(20) UNIQUE NOT NULL,
                    descricao TEXT NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    localizacao_atual VARCHAR(100) NOT NULL,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario_cadastro INTEGER REFERENCES usuarios(id)
                )
                ''',
                
                # Tabela historico_movimentacao
                '''
                CREATE TABLE IF NOT EXISTS historico_movimentacao (
                    id SERIAL PRIMARY KEY,
                    patrimonio_id INTEGER REFERENCES patrimonios(id),
                    localizacao_anterior VARCHAR(100),
                    localizacao_nova VARCHAR(100) NOT NULL,
                    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario_movimentacao INTEGER REFERENCES usuarios(id),
                    observacao TEXT
                )
                ''',
                
                # Tabela leilao_patrimonios
                '''
                CREATE TABLE IF NOT EXISTS leilao_patrimonios (
                    id SERIAL PRIMARY KEY,
                    patrimonio_id INTEGER UNIQUE REFERENCES patrimonios(id),
                    numero_patrimonio VARCHAR(20) UNIQUE NOT NULL,
                    descricao TEXT NOT NULL,
                    estado VARCHAR(50) NOT NULL,
                    motivo_descarte TEXT,
                    data_entrada_leilao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario_responsavel INTEGER REFERENCES usuarios(id),
                    observacoes TEXT
                )
                ''',
                
                # Tabela planilha_comparacao
                '''
                CREATE TABLE IF NOT EXISTS planilha_comparacao (
                    id SERIAL PRIMARY KEY,
                    numero_patrimonio VARCHAR(20) NOT NULL,
                    descricao TEXT,
                    localizacao_planilha VARCHAR(100),
                    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usuario_upload INTEGER REFERENCES usuarios(id)
                )
                '''
            ]
            
            for sql in tabelas_sql:
                try:
                    cur.execute(sql)
                    print("  ✅ Tabela criada/verificada")
                except Exception as e:
                    print(f"  ⚠️  Erro na tabela: {e}")
            
            # Verificar/criar usuário admin
            cur.execute("SELECT id FROM usuarios WHERE username = 'admin'")
            if not cur.fetchone():
                password_hash = generate_password_hash('admin123')
                cur.execute(
                    "INSERT INTO usuarios (username, password_hash, nome_completo, email) VALUES (%s, %s, %s, %s)",
                    ('admin', password_hash, 'Administrador', 'admin@gepat.com')
                )
                print("  ✅ Usuário admin criado")
            else:
                print("  ✅ Usuário admin já existe")
            
            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ Erro no {config['NOME']}: {e}")

if __name__ == '__main__':
    init_databases()