## GEPAT
O GEPAT é um sistema web para gerenciamento de patrimônios da Perícia Médica com controle de acesso, histórico de movimentações, relatórios em Excel e um comparativo com a Guia de Patrimônio da DRFPA e o GEPAT para verificar se está tudo em conformidade.

# Funcionalidades

- Autenticação segura com usuário e senha

- CRUD completo de patrimônios

- Histórico de movimentações automático

- Relatórios em Excel para download

- Controle de usuários e permissões

- Interface web responsiva com Bootstrap

- Banco de dados PostgreSQL

# Como executar o projeto

- Pré-requisitos: Python 3.8+

- PostgreSQL

Git:

- Clone o repositório bash git clone cd gepat

- Instale as dependências Python bash pip install -r requirements.txt

- Inicie o banco de dados PostgreSQL

- Acesse o sistema URL:

  https://localhost:5000 para desenvolvimento

  https://10.16.90.70:5000 para produção

Usuário padrão: admin / senha: admin123

Execute os arquivos na ordem:

- init_admin.py

- init_database.py

- create_admin_both.py

- sync_users.py

- app.py


# ESTRUTURA DO PROJETO

GEPAT/

├── app.py

├── database.py

├── auth.py

├── models.py

├── config.py

├── create_admin_both.py

├── init_database.py

├── sync_users.py

├── static/

│   ├── css/

│   │   └── style.css

│   └── js/

│       └── script.js

├── templates/

│   ├── base.html

│   ├── comparação.html

│   ├── login.html

│   ├── dashboard.html

│   ├── patrimonios.html

│   ├── usuarios.html

│   └── historico.html

│   ├── selecionar_setor.html

│   ├── leilão.html

└── requirements.txt

# Sistema de Autenticação

•	Usuários Padrão Administrador: admin / admin123 - Acesso completo

•	Usuário: usuario / user123 - Acesso básico

•	Permissões Administradores: Cadastram usuários, acessam todas as funcionalidades

•	Usuários normais: Gerenciam patrimônios, geram relatórios


# Modelo de Dados

•	Tabelas Principais Usuario id, username, email, password_hash, nome, departamento

•	ativo, data_criacao, is_admin

•	Patrimonio id, patrimonio (número único), descricao, localizacao

•	status (em uso/disponível), data_cadastro, usuario_cadastro_id

•	Movimentacao id, patrimonio_id, usuario_id, data_movimentacao

•	origem, destino, observacao


# Relatórios Disponíveis

•	Relatório Simples Lista básica de todos os patrimônios

  o	Inclui: número, descrição, localização, status, data de cadastro

•	Relatório Detalhado Histórico completo de movimentações

  o	Múltiplas abas no Excel (Patrimônios + Movimentações)

•	Relatório Filtrado Filtros por status e localização
  
  o	Exportação personalizada

# Licença

Este projeto foi desenvolvido para uso interno da Perícia Médica.

# Suporte

Em caso de problemas:

•	Confirme que as dependências Python estão instaladas

•	Execute os scripts de manutenção 
•	Verifique os logs no terminal da aplicação
•	Desenvolvido para Perícia Médica Versão: 1.0 Última atualização: 2025
