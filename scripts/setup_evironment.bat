@echo off
echo ====================================
echo    CONFIGURACAO GEPAT - PRODUCAO
echo ====================================
echo.

echo 1. Instalando dependencias Python...
pip install -r requirements.txt

echo.
echo 2. Criando estrutura de pastas...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs

echo.
echo 3. Configurando bancos de dados...
python init_database.py

echo.
echo 4. Sincronizando usuarios...
python sync_users.py

echo.
echo ✅ CONFIGURACAO CONCLUIDA!
echo.
echo Para iniciar o servidor:
echo python app.py
echo.
pause