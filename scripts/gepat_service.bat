@echo off
title GEPAT Servidor - 10.16.90.70:5000
echo ====================================
echo    GEPAT - SERVIDOR DE PRODUCAO
echo ====================================
echo Endereco: http://10.16.90.70:5000
echo Data: %date% %time%
echo ====================================
echo.

cd /d C:\GEPAT
python app.py

pause