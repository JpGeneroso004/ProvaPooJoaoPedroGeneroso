@echo off
title Art.Tendas - Sistema de Gestao
color 0A
cd /d "%~dp0arttendas"

echo.
echo  ==========================================
echo    ART.TENDAS - Sistema de Gestao
echo  ==========================================
echo.

:: Verifica Python
py --version >nul 2>&1
if errorlevel 1 (
    echo  [ERRO] Python nao encontrado!
    echo  Instale em: https://python.org/downloads
    pause & exit
)

:: Instala dependencias
echo  [1/4] Instalando dependencias...
py -m pip install django pillow --quiet --disable-pip-version-check

:: Migrations
echo  [2/4] Criando banco de dados...
py manage.py makemigrations inventario --no-input >nul 2>&1
py manage.py makemigrations eventos --no-input >nul 2>&1
py manage.py migrate --no-input

:: Seed de demonstracao
echo  [3/4] Carregando dados...
py manage.py seed_data

:: Abre navegador e inicia servidor
echo  [4/4] Iniciando servidor...
echo.
echo  ==========================================
echo    Acesse: http://127.0.0.1:8000
echo    Para encerrar: feche esta janela
echo  ==========================================
echo.
start "" http://127.0.0.1:8000
py manage.py runserver
