class Config:
    # Configurações comuns
    SECRET_KEY = 'gepat2024-multisetor'
    
    # Configurações por setor
    SETORES = {
        'ti': {
            'DB_HOST': 'localhost',
            'DB_NAME': 'gepat_db',
            'DB_USER': 'gepat_user',
            'DB_PASSWORD': 'gepat123',
            'DB_PORT': '5432',
            'NOME': 'Setor de TI',
            'COR': 'primary'
        },
        'apoio_logistico': {
            'DB_HOST': 'localhost',
            'DB_NAME': 'gepat_apoio_logistico',
            'DB_USER': 'gepat_user',
            'DB_PASSWORD': 'gepat123',
            'DB_PORT': '5432',
            'NOME': 'Apoio Logístico',
            'COR': 'success'
        }
    }
    
    @staticmethod
    def get_config(setor):
        return Config.SETORES.get(setor, Config.SETORES['ti'])