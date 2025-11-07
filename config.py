class Config:
    # Configurações comuns - MUDAR PARA UMA CHAVE SEGURA!
    SECRET_KEY = 'gepat-producao-2024-chave-super-segura-mudar-isso'
    
    # Configurações por setor
    SETORES = {
        'ti': {
            'DB_HOST': 'localhost',
            'DB_NAME': 'gepat_db',
            'DB_USER': 'gepat_user',
            'DB_PASSWORD': 'gepat123',  # ALTERE PARA SUA SENHA
            'DB_PORT': '5432',
            'NOME': 'Setor de TI',
            'COR': 'primary'
        },
        'apoio_logistico': {
            'DB_HOST': 'localhost',
            'DB_NAME': 'gepat_apoio_logistico',
            'DB_USER': 'gepat_user',
            'DB_PASSWORD': 'gepat123',  # ALTERE PARA SUA SENHA
            'DB_PORT': '5432',
            'NOME': 'Apoio Logístico',
            'COR': 'success'
        }
    }
    
    @staticmethod
    def get_config(setor):
        return Config.SETORES.get(setor, Config.SETORES['ti'])