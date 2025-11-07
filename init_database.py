# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys
from werkzeug.security import generate_password_hash

def create_database_and_tables():
    try:
        print("Conectando ao PostgreSQL...")
        
        # Conectar ao PostgreSQL para criar o banco
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password='administrador',  # Altere para sua senha do PostgreSQL
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        print("Verificando se o banco de dados existe...")
        
        # Criar banco de dados se não existir
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'gepat_db'")
        exists = cur.fetchone()
        
        if not exists:
            print("Criando banco de dados 'gepat_db'...")
            cur.execute('CREATE DATABASE gepat_db')
            print("✓ Banco de dados 'gepat_db' criado com sucesso!")
        else:
            print("✓ Banco de dados 'gepat_db' já existe.")
        
        cur.close()
        conn.close()
        
        # Agora conectar ao banco gepat_db para criar as tabelas
        print("Conectando ao banco gepat_db...")
        conn = psycopg2.connect(
            host='localhost',
            database='gepat_db',
            user='postgres',
            password='administrador',  # Altere para sua senha do PostgreSQL
            port='5432'
        )
        cur = conn.cursor()
        
        print("Criando tabelas...")
        
        # Criar tabela de usuários
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                nome_completo VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                ativo BOOLEAN DEFAULT TRUE,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Tabela 'usuarios' criada/verificada")
        
        # Criar tabela de patrimônios
        cur.execute('''
            CREATE TABLE IF NOT EXISTS patrimonios (
                id SERIAL PRIMARY KEY,
                numero_patrimonio VARCHAR(20) UNIQUE NOT NULL,
                descricao TEXT NOT NULL,
                status VARCHAR(50) NOT NULL,
                localizacao_atual VARCHAR(100) NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_cadastro INTEGER REFERENCES usuarios(id)
            )
        ''')
        print("✓ Tabela 'patrimonios' criada/verificada")
        
        # Criar tabela de histórico de movimentação
        cur.execute('''
            CREATE TABLE IF NOT EXISTS historico_movimentacao (
                id SERIAL PRIMARY KEY,
                patrimonio_id INTEGER REFERENCES patrimonios(id),
                localizacao_anterior VARCHAR(100),
                localizacao_nova VARCHAR(100) NOT NULL,
                data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_movimentacao INTEGER REFERENCES usuarios(id),
                observacao TEXT
            )
        ''')
        print("✓ Tabela 'historico_movimentacao' criada/verificada")
        
        # Verificar se o usuário admin já existe
        print("Verificando usuário admin...")
        cur.execute("SELECT COUNT(*) FROM usuarios WHERE username = 'admin'")
        admin_count = cur.fetchone()[0]
        
        if admin_count == 0:
            password_hash = generate_password_hash('admin123')
            
            cur.execute('''
                INSERT INTO usuarios (username, password_hash, nome_completo, email) 
                VALUES (%s, %s, %s, %s)
            ''', ('admin', password_hash, 'Administrador', 'admin@gepat.com'))
            
            print("✓ Usuário admin criado com sucesso!")
            print("  Usuário: admin")
            print("  Senha: admin123")
        else:
            print("✓ Usuário admin já existe")
        
        conn.commit()
        print("\n" + "="*50)
        print("✓ INICIALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*50)
        print("Banco: gepat_db")
        print("Host: localhost:5432")
        print("Usuário padrão: admin / admin123")
        print("="*50)
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ ERRO DE CONEXÃO: {e}")
        print("\nSolução:")
        print("1. Verifique se o PostgreSQL está rodando")
        print("2. Confirme as credenciais no script")
        print("3. Altere a senha no script para a senha do seu PostgreSQL")
        
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    create_database_and_tables()
    
    input("\nPressione Enter para sair...")