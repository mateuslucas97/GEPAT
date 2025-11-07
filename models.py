from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash  # ADICIONAR generate_password_hash
from database import get_db_connection, get_db_connection_login
import pandas as pd
from werkzeug.utils import secure_filename
import os

class User(UserMixin):
    def __init__(self, id, username, nome_completo, email, ativo=True):
        self.id = id
        self.username = username
        self.nome_completo = nome_completo
        self.email = email
        self.ativo = ativo

    @staticmethod
    def get(user_id):
        # Sempre busca no banco de login (TI)
        conn = get_db_connection_login()
        if not conn:
            return None
            
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if user_data:
            return User(
                id=user_data[0],
                username=user_data[1],
                nome_completo=user_data[3],
                email=user_data[4],
                ativo=user_data[5]
            )
        return None

    @staticmethod
    def authenticate(username, password):
        # Sempre autentica no banco de login (TI)
        conn = get_db_connection_login()
        if not conn:
            return None
            
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios WHERE username = %s AND ativo = true', (username,))
        user_data = cur.fetchone()
        
        if user_data and check_password_hash(user_data[2], password):
            user = User(
                id=user_data[0],
                username=user_data[1],
                nome_completo=user_data[3],
                email=user_data[4],
                ativo=user_data[5]
            )
            cur.close()
            conn.close()
            return user
        
        cur.close()
        conn.close()
        return None

    @staticmethod
    def create(username, password, nome_completo, email):
        # Sempre cria no banco de login (TI)
        conn = get_db_connection_login()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            password_hash = generate_password_hash(password)
            cur.execute(
                'INSERT INTO usuarios (username, password_hash, nome_completo, email) VALUES (%s, %s, %s, %s)',
                (username, password_hash, nome_completo, email)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar usuario: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all():
        # Sempre busca todos do banco de login (TI)
        conn = get_db_connection_login()
        if not conn:
            return []
            
        cur = conn.cursor()
        cur.execute('SELECT id, username, nome_completo, email, ativo, data_criacao FROM usuarios ORDER BY id')
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        return usuarios

    @staticmethod
    def toggle_status(user_id):
        # Sempre altera status no banco de login (TI)
        conn = get_db_connection_login()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            # Buscar status atual
            cur.execute('SELECT ativo FROM usuarios WHERE id = %s', (user_id,))
            result = cur.fetchone()
            if not result:
                return False
                
            novo_status = not result[0]
            cur.execute('UPDATE usuarios SET ativo = %s WHERE id = %s', (novo_status, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao alterar status do usuario: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

class Patrimonio:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        if not conn:
            return []
            
        cur = conn.cursor()
        cur.execute('SELECT * FROM patrimonios ORDER BY data_cadastro DESC')
        patrimonios = cur.fetchall()
        cur.close()
        conn.close()
        return patrimonios

    @staticmethod
    def get_by_id(patrimonio_id):
        conn = get_db_connection()
        if not conn:
            return None
            
        cur = conn.cursor()
        cur.execute('SELECT * FROM patrimonios WHERE id = %s', (patrimonio_id,))
        patrimonio = cur.fetchone()
        cur.close()
        conn.close()
        return patrimonio

    @staticmethod
    def create(numero_patrimonio, descricao, status, localizacao, usuario_id):
        conn = get_db_connection()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO patrimonios (numero_patrimonio, descricao, status, localizacao_atual, usuario_cadastro) VALUES (%s, %s, %s, %s, %s)',
                (numero_patrimonio, descricao, status, localizacao, usuario_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar patrimonio: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update(patrimonio_id, descricao, status, localizacao, usuario_id):
        conn = get_db_connection()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            # Primeiro buscar a localização atual para registrar no histórico
            cur.execute('SELECT localizacao_atual FROM patrimonios WHERE id = %s', (patrimonio_id,))
            resultado = cur.fetchone()
            localizacao_anterior = resultado[0] if resultado else ''
            
            # Atualizar o patrimônio
            cur.execute(
                'UPDATE patrimonios SET descricao = %s, status = %s, localizacao_atual = %s WHERE id = %s',
                (descricao, status, localizacao, patrimonio_id)
            )
            
            # Registrar no histórico se a localização mudou
            if localizacao_anterior and localizacao_anterior != localizacao:
                cur.execute(
                    'INSERT INTO historico_movimentacao (patrimonio_id, localizacao_anterior, localizacao_nova, usuario_movimentacao) VALUES (%s, %s, %s, %s)',
                    (patrimonio_id, localizacao_anterior, localizacao, usuario_id)
                )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar patrimonio: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete(patrimonio_id):
        conn = get_db_connection()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            # Primeiro deletar o histórico associado
            cur.execute('DELETE FROM historico_movimentacao WHERE patrimonio_id = %s', (patrimonio_id,))
            # Depois deletar o patrimônio
            cur.execute('DELETE FROM patrimonios WHERE id = %s', (patrimonio_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar patrimonio: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

class LeilaoPatrimonio:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        if not conn:
            return []
            
        cur = conn.cursor()
        cur.execute('''
            SELECT lp.*, u.nome_completo 
            FROM leilao_patrimonios lp 
            LEFT JOIN usuarios u ON lp.usuario_responsavel = u.id 
            ORDER BY lp.data_entrada_leilao DESC
        ''')
        leilao_patrimonios = cur.fetchall()
        cur.close()
        conn.close()
        return leilao_patrimonios

    @staticmethod
    def get_by_id(leilao_id):
        conn = get_db_connection()
        if not conn:
            return None
            
        cur = conn.cursor()
        cur.execute('SELECT * FROM leilao_patrimonios WHERE id = %s', (leilao_id,))
        patrimonio = cur.fetchone()
        cur.close()
        conn.close()
        return patrimonio

    @staticmethod
    def transferir_para_leilao(patrimonio_id, estado, motivo_descarte, observacoes, usuario_id):
        conn = get_db_connection()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            # Buscar dados do patrimônio
            cur.execute('SELECT numero_patrimonio, descricao FROM patrimonios WHERE id = %s', (patrimonio_id,))
            patrimonio_data = cur.fetchone()
            
            if not patrimonio_data:
                return False
            
            numero_patrimonio, descricao = patrimonio_data
            
            # Verificar se já existe no leilão
            cur.execute('SELECT id FROM leilao_patrimonios WHERE patrimonio_id = %s', (patrimonio_id,))
            if cur.fetchone():
                return False  # Já está no leilão
            
            # Inserir na tabela de leilão
            cur.execute('''
                INSERT INTO leilao_patrimonios 
                (patrimonio_id, numero_patrimonio, descricao, estado, motivo_descarte, usuario_responsavel, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (patrimonio_id, numero_patrimonio, descricao, estado, motivo_descarte, usuario_id, observacoes))
            
            # Atualizar status do patrimônio para "em leilão"
            cur.execute('UPDATE patrimonios SET status = %s WHERE id = %s', ('em leilao', patrimonio_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao transferir para leilão: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def retornar_para_patrimonios(leilao_id, usuario_id):
        conn = get_db_connection()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            # Buscar dados do leilão
            cur.execute('SELECT patrimonio_id FROM leilao_patrimonios WHERE id = %s', (leilao_id,))
            leilao_data = cur.fetchone()
            
            if not leilao_data:
                return False
            
            patrimonio_id = leilao_data[0]
            
            # Atualizar status do patrimônio de volta para "disponível"
            cur.execute('UPDATE patrimonios SET status = %s WHERE id = %s', ('disponivel', patrimonio_id))
            
            # Deletar da tabela de leilão
            cur.execute('DELETE FROM leilao_patrimonios WHERE id = %s', (leilao_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao retornar para patrimônios: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def deletar_do_leilao(leilao_id):
        conn = get_db_connection()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            # Primeiro retornar o status do patrimônio
            cur.execute('SELECT patrimonio_id FROM leilao_patrimonios WHERE id = %s', (leilao_id,))
            leilao_data = cur.fetchone()
            
            if leilao_data:
                patrimonio_id = leilao_data[0]
                cur.execute('UPDATE patrimonios SET status = %s WHERE id = %s', ('disponivel', patrimonio_id))
            
            # Depois deletar do leilão
            cur.execute('DELETE FROM leilao_patrimonios WHERE id = %s', (leilao_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar do leilão: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def cadastrar_direto_leilao(numero_patrimonio, descricao, estado, motivo_descarte, observacoes, usuario_id):
        conn = get_db_connection()
        if not conn:
            return False
            
        cur = conn.cursor()
        try:
            # Verificar se o número de patrimônio já existe no leilão
            cur.execute('SELECT id FROM leilao_patrimonios WHERE numero_patrimonio = %s', (numero_patrimonio,))
            if cur.fetchone():
                return False  # Já existe no leilão
            
            # Verificar se o número de patrimônio existe nos patrimônios comuns
            cur.execute('SELECT id FROM patrimonios WHERE numero_patrimonio = %s', (numero_patrimonio,))
            patrimonio_existente = cur.fetchone()
            
            if patrimonio_existente:
                # Se existe nos patrimônios comuns, transferir para leilão
                patrimonio_id = patrimonio_existente[0]
                
                # Inserir na tabela de leilão
                cur.execute('''
                    INSERT INTO leilao_patrimonios 
                    (patrimonio_id, numero_patrimonio, descricao, estado, motivo_descarte, usuario_responsavel, observacoes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (patrimonio_id, numero_patrimonio, descricao, estado, motivo_descarte, usuario_id, observacoes))
                
                # Atualizar status do patrimônio para "em leilão"
                cur.execute('UPDATE patrimonios SET status = %s WHERE id = %s', ('em leilao', patrimonio_id))
            else:
                # Se não existe, cadastrar diretamente no leilão (sem patrimonio_id)
                cur.execute('''
                    INSERT INTO leilao_patrimonios 
                    (numero_patrimonio, descricao, estado, motivo_descarte, usuario_responsavel, observacoes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (numero_patrimonio, descricao, estado, motivo_descarte, usuario_id, observacoes))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar direto no leilão: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

class PlanilhaComparacao:
    @staticmethod
    def processar_planilha(arquivo, usuario_id):
        try:
            # Ler a planilha Excel
            df = pd.read_excel(arquivo)
            
            # Verificar se as colunas necessárias existem
            colunas_necessarias = ['numero_patrimonio']
            colunas_opcionais = ['descricao', 'localizacao']
            
            # Verificar colunas
            colunas_planilha = df.columns.str.lower().tolist()
            
            # Mapear colunas (case insensitive)
            mapeamento_colunas = {}
            for coluna in colunas_necessarias + colunas_opcionais:
                for col_planilha in colunas_planilha:
                    if coluna in col_planilha.lower():
                        mapeamento_colunas[coluna] = col_planilha
                        break
            
            # Verificar se tem pelo menos a coluna número de patrimônio
            if 'numero_patrimonio' not in mapeamento_colunas:
                return False, "Coluna 'numero_patrimonio' não encontrada na planilha"
            
            conn = get_db_connection()
            if not conn:
                return False, "Erro de conexão com o banco"
            
            cur = conn.cursor()
            
            # Limpar dados anteriores do mesmo usuário
            cur.execute('DELETE FROM planilha_comparacao WHERE usuario_upload = %s', (usuario_id,))
            
            # Inserir novos dados
            for index, row in df.iterrows():
                numero_patrimonio = str(row[mapeamento_colunas['numero_patrimonio']]).strip()
                
                # Pular linhas vazias
                if pd.isna(numero_patrimonio) or numero_patrimonio == 'nan' or not numero_patrimonio:
                    continue
                
                descricao = ''
                if 'descricao' in mapeamento_colunas:
                    descricao_valor = row[mapeamento_colunas['descricao']]
                    descricao = str(descricao_valor) if not pd.isna(descricao_valor) else ''
                
                localizacao = ''
                if 'localizacao' in mapeamento_colunas:
                    localizacao_valor = row[mapeamento_colunas['localizacao']]
                    localizacao = str(localizacao_valor) if not pd.isna(localizacao_valor) else ''
                
                cur.execute('''
                    INSERT INTO planilha_comparacao 
                    (numero_patrimonio, descricao, localizacao_planilha, usuario_upload)
                    VALUES (%s, %s, %s, %s)
                ''', (numero_patrimonio, descricao, localizacao, usuario_id))
            
            conn.commit()
            cur.close()
            conn.close()
            
            return True, "Planilha processada com sucesso"
            
        except Exception as e:
            print(f"Erro ao processar planilha: {e}")
            return False, f"Erro ao processar planilha: {str(e)}"

    @staticmethod
    def comparar_com_gepat(usuario_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cur = conn.cursor()
            
            # Buscar patrimônios da planilha
            cur.execute('''
                SELECT numero_patrimonio, descricao, localizacao_planilha 
                FROM planilha_comparacao 
                WHERE usuario_upload = %s
            ''', (usuario_id,))
            planilha_patrimonios = cur.fetchall()
            
            # Buscar patrimônios do GEPAT (excluindo os em leilão)
            cur.execute('''
                SELECT numero_patrimonio, descricao, localizacao_atual, status
                FROM patrimonios 
                WHERE status != 'em leilao'
            ''')
            gepat_patrimonios = cur.fetchall()
            
            # Converter para conjuntos para comparação
            planilha_numeros = {str(pat[0]).strip() for pat in planilha_patrimonios}
            gepat_numeros = {str(pat[0]).strip() for pat in gepat_patrimonios}
            
            # Encontrar diferenças
            nao_encontrados_gepat = planilha_numeros - gepat_numeros
            nao_encontrados_planilha = gepat_numeros - planilha_numeros
            
            # Buscar detalhes dos patrimônios não encontrados
            detalhes_nao_encontrados_gepat = []
            for patrimonio in planilha_patrimonios:
                if str(patrimonio[0]).strip() in nao_encontrados_gepat:
                    detalhes_nao_encontrados_gepat.append({
                        'numero_patrimonio': patrimonio[0],
                        'descricao': patrimonio[1],
                        'localizacao_planilha': patrimonio[2]
                    })
            
            detalhes_nao_encontrados_planilha = []
            for patrimonio in gepat_patrimonios:
                if str(patrimonio[0]).strip() in nao_encontrados_planilha:
                    detalhes_nao_encontrados_planilha.append({
                        'numero_patrimonio': patrimonio[0],
                        'descricao': patrimonio[1],
                        'localizacao_atual': patrimonio[2],
                        'status': patrimonio[3]
                    })
            
            resultado = {
                'total_planilha': len(planilha_numeros),
                'total_gepat': len(gepat_numeros),
                'comuns': len(planilha_numeros & gepat_numeros),
                'nao_encontrados_gepat': detalhes_nao_encontrados_gepat,
                'nao_encontrados_planilha': detalhes_nao_encontrados_planilha,
                'conformidade': len(planilha_numeros & gepat_numeros) == len(planilha_numeros) == len(gepat_numeros)
            }
            
            return resultado
            
        except Exception as e:
            print(f"Erro na comparação: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def limpar_comparacao(usuario_id):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM planilha_comparacao WHERE usuario_upload = %s', (usuario_id,))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao limpar comparação: {e}")
            return False