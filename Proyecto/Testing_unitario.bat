@echo off

python script_db_check.py

echo Ejecutando pruebas
python -m unittest discover -s tests