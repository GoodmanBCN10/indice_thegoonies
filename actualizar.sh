#!/bin/bash

# Script para ejecutar el bot desde un VPS y subir los cambios a GitHub
# (Índice de Juegos)

cd "$(dirname "$0")"

# 1. Asegurarnos de tener la última versión del código
git pull

# 2. Activar el entorno virtual si lo usas (descomenta la siguiente línea)
# source venv/bin/activate

# 3. Ejecutar el bot
python generar_indice.py

# 4. Guardar y subir cambios si los hay
git add indice_juegos.json index.html

# Comprobar si hay cambios para evitar errores al hacer commit vacío
if ! git diff --staged --quiet; then
    git commit -m "Automatización: Índice de juegos actualizado desde VPS [skip ci]"
    git push
else
    echo "No hay juegos nuevos en el índice."
fi
