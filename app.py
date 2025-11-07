from flask import Flask, render_template, request, jsonify, redirect, session
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_required, current_user
from database import get_db_connection, get_config_setor
from models import User, Patrimonio, LeilaoPatrimonio, PlanilhaComparacao
from auth import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gepat2024-multisetor-segura'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

app.register_blueprint(auth_bp)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Função auxiliar para obter config_setor de forma segura
def get_safe_config_setor():
    """Obtém config_setor de forma segura, mesmo sem sessão"""
    try:
        return get_config_setor()
    except:
        from config import Config
        return Config.get_config('ti')

@app.route('/')
def main_index():
    if current_user.is_authenticated:
        if session.get('setor'):
            return redirect('/dashboard')
        else:
            return redirect('/selecionar-setor')
    else:
        return redirect('/login')

@app.route('/selecionar-setor', methods=['GET', 'POST'])
@login_required
def selecionar_setor():
    if request.method == 'POST':
        setor = request.form.get('setor')
        if setor in ['ti', 'apoio_logistico']:
            session['setor'] = setor
            return redirect('/dashboard')
    
    config_setor = get_safe_config_setor()
    return render_template('selecionar_setor.html', config_setor=config_setor)

@app.route('/trocar-setor')
@login_required
def trocar_setor():
    session.pop('setor', None)
    return redirect('/selecionar-setor')

@app.route('/dashboard')
@login_required
def dashboard():
    if not session.get('setor'):
        return redirect('/selecionar-setor')
    
    patrimonios = Patrimonio.get_all()
    config_setor = get_safe_config_setor()
    return render_template('dashboard.html', patrimonios=patrimonios, config_setor=config_setor)

@app.route('/patrimonios')
@login_required
def patrimonios():
    if not session.get('setor'):
        return redirect('/selecionar-setor')
    
    patrimonios_list = Patrimonio.get_all()
    config_setor = get_safe_config_setor()
    return render_template('patrimonios.html', patrimonios=patrimonios_list, config_setor=config_setor)

@app.route('/api/patrimonios', methods=['POST'])
@login_required
def create_patrimonio():
    data = request.get_json()
    success = Patrimonio.create(
        data['numero_patrimonio'],
        data['descricao'],
        data['status'],
        data['localizacao'],
        current_user.id
    )
    
    if success:
        return jsonify({'success': True, 'message': 'Patrimonio criado'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao criar'})

@app.route('/api/patrimonios/<int:patrimonio_id>', methods=['GET'])
@login_required
def get_patrimonio(patrimonio_id):
    patrimonio = Patrimonio.get_by_id(patrimonio_id)
    if patrimonio:
        return jsonify({
            'success': True,
            'patrimonio': {
                'id': patrimonio[0],
                'numero_patrimonio': patrimonio[1],
                'descricao': patrimonio[2],
                'status': patrimonio[3],
                'localizacao': patrimonio[4]
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Patrimonio nao encontrado'})

@app.route('/api/patrimonios/<int:patrimonio_id>', methods=['PUT'])
@login_required
def update_patrimonio(patrimonio_id):
    data = request.get_json()
    
    success = Patrimonio.update(
        patrimonio_id,
        data['descricao'],
        data['status'],
        data['localizacao'],
        current_user.id
    )
    
    if success:
        return jsonify({'success': True, 'message': 'Patrimonio atualizado com sucesso!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao atualizar patrimonio'})

@app.route('/api/patrimonios/<int:patrimonio_id>', methods=['DELETE'])
@login_required
def delete_patrimonio(patrimonio_id):
    success = Patrimonio.delete(patrimonio_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Patrimonio deletado com sucesso!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao deletar patrimonio'})

@app.route('/leilao')
@login_required
def leilao():
    if not session.get('setor'):
        return redirect('/selecionar-setor')
    
    leilao_patrimonios = LeilaoPatrimonio.get_all()
    config_setor = get_safe_config_setor()
    return render_template('leilao.html', leilao_patrimonios=leilao_patrimonios, config_setor=config_setor)

@app.route('/api/leilao/transferir', methods=['POST'])
@login_required
def transferir_para_leilao():
    data = request.get_json()
    
    success = LeilaoPatrimonio.transferir_para_leilao(
        data['patrimonio_id'],
        data['estado'],
        data['motivo_descarte'],
        data.get('observacoes', ''),
        current_user.id
    )
    
    if success:
        return jsonify({'success': True, 'message': 'Patrimonio transferido para leilão com sucesso!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao transferir para leilão'})

@app.route('/api/leilao/<int:leilao_id>/retornar', methods=['POST'])
@login_required
def retornar_para_patrimonios(leilao_id):
    success = LeilaoPatrimonio.retornar_para_patrimonios(leilao_id, current_user.id)
    
    if success:
        return jsonify({'success': True, 'message': 'Patrimonio retornado para lista comum!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao retornar patrimonio'})

@app.route('/api/leilao/<int:leilao_id>', methods=['DELETE'])
@login_required
def deletar_do_leilao(leilao_id):
    success = LeilaoPatrimonio.deletar_do_leilao(leilao_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Patrimonio removido do leilão!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao remover do leilão'})

@app.route('/api/leilao/cadastrar-direto', methods=['POST'])
@login_required
def cadastrar_direto_leilao():
    data = request.get_json()
    
    if not all([data.get('numero_patrimonio'), data.get('descricao'), data.get('estado'), data.get('motivo_descarte')]):
        return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios'})
    
    success = LeilaoPatrimonio.cadastrar_direto_leilao(
        data['numero_patrimonio'],
        data['descricao'],
        data['estado'],
        data['motivo_descarte'],
        data.get('observacoes', ''),
        current_user.id
    )
    
    if success:
        return jsonify({'success': True, 'message': 'Patrimonio cadastrado no leilão com sucesso!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao cadastrar no leilão. Número de patrimônio já existe.'})

@app.route('/comparacao')
@login_required
def comparacao():
    if not session.get('setor'):
        return redirect('/selecionar-setor')
    
    config_setor = get_safe_config_setor()
    return render_template('comparacao.html', config_setor=config_setor)

@app.route('/api/comparacao/upload', methods=['POST'])
@login_required
def upload_planilha():
    if 'planilha' not in request.files:
        return jsonify({'success': False, 'message': 'Nenhum arquivo selecionado'})
    
    file = request.files['planilha']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Nenhum arquivo selecionado'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        success, message = PlanilhaComparacao.processar_planilha(filepath, current_user.id)
        
        try:
            os.remove(filepath)
        except:
            pass
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message})
    
    return jsonify({'success': False, 'message': 'Tipo de arquivo não permitido'})

@app.route('/api/comparacao/resultado')
@login_required
def get_resultado_comparacao():
    resultado = PlanilhaComparacao.comparar_com_gepat(current_user.id)
    
    if resultado:
        return jsonify({'success': True, 'resultado': resultado})
    else:
        return jsonify({'success': False, 'message': 'Erro ao realizar comparação'})

@app.route('/api/comparacao/limpar', methods=['POST'])
@login_required
def limpar_comparacao():
    success = PlanilhaComparacao.limpar_comparacao(current_user.id)
    
    if success:
        return jsonify({'success': True, 'message': 'Dados de comparação limpos'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao limpar dados'})

@app.route('/historico')
@login_required
def historico():
    if not session.get('setor'):
        return redirect('/selecionar-setor')
    
    conn = get_db_connection()
    if not conn:
        return "Erro banco"
        
    cur = conn.cursor()
    cur.execute('''
        SELECT hm.*, p.numero_patrimonio, p.descricao 
        FROM historico_movimentacao hm 
        JOIN patrimonios p ON hm.patrimonio_id = p.id 
        ORDER BY hm.data_movimentacao DESC
    ''')
    historico = cur.fetchall()
    cur.close()
    conn.close()
    
    config_setor = get_safe_config_setor()
    return render_template('historico.html', historico=historico, config_setor=config_setor)

@app.route('/usuarios')
@login_required
def usuarios():
    if not session.get('setor'):
        return redirect('/selecionar-setor')
    
    usuarios_list = User.get_all()
    config_setor = get_safe_config_setor()
    return render_template('usuarios.html', usuarios=usuarios_list, config_setor=config_setor)

@app.route('/api/usuarios', methods=['POST'])
@login_required
def create_usuario():
    data = request.get_json()
    
    if not all([data.get('username'), data.get('password'), data.get('nome_completo')]):
        return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatorios'})
    
    success = User.create(
        data['username'],
        data['password'],
        data['nome_completo'],
        data.get('email', '')
    )
    
    if success:
        return jsonify({'success': True, 'message': 'Usuario criado com sucesso!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao criar usuario. Username ja existe.'})

@app.route('/api/usuarios/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_usuario_status(user_id):
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'Nao pode desativar seu proprio usuario'})
    
    success = User.toggle_status(user_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Status do usuario atualizado!'})
    else:
        return jsonify({'success': False, 'message': 'Erro ao atualizar status'})

if __name__ == '__main__':
    print("App GEPAT Multi-Setor iniciando...")
    app.run(debug=True, host='localhost', port=5000)