import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from flask import session, has_request_context

def get_db_connection(setor=None):
    """Estabelece conexão com o banco de dados do setor especificado ou atual"""
    if not setor:
        if has_request_context() and session:
            setor = session.get('setor', 'ti')
        else:
            setor = 'ti'
    
    config = Config.get_config(setor)
    
    try:
        conn = psycopg2.connect(
            host=config['DB_HOST'],
            database=config['DB_NAME'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            port=config['DB_PORT']
        )
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar com o banco do setor {setor}: {e}")
        return None

def get_db_connection_login():
    """Conexão específica para login - sempre usa banco de TI"""
    return get_db_connection('ti')

def get_setor_atual():
    """Retorna o setor atual de forma segura"""
    if has_request_context() and session:
        return session.get('setor', 'ti')
    return 'ti'

def get_config_setor():
    """Retorna a configuração do setor atual de forma segura"""
    setor_atual = get_setor_atual()
    return Config.get_config(setor_atual)